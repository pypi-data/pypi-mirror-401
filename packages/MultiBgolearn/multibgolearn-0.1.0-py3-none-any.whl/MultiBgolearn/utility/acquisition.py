import numpy as np
from .funs import get_pareto_front, calculate_lebesgue_measure,Monte_Carlo,imp_prob,imp_ucb


def multi_BGO(y, vs_mean, vs_vars, method, max_search=True, times=10, batch_size=1, noise_std=None):
    """
    Perform Multi-BGO optimization.

    :param y: training targets
    :param vs_mean: means of virtual data points
    :param vs_vars: variances of virtual data points
    :param method: Multi-BGO method (e.g., 'EHVI', 'qNEHVI')
    :param max_search: whether to perform maximization (True) or minimization (False)
    :param times: number of Monte Carlo samples
    :param batch_size: number of points to select simultaneously (for batch methods like qNEHVI)
    :param noise_std: observation noise standard deviation for qNEHVI (if None, estimated from data)
    :return: index of the virtual data point with the highest expected improvement (or indices for batch methods)
    """
    if method == 'EHVI':
        # Calculate the current Pareto front based on the training targets
        pareto_front = get_pareto_front(y,max_search)
        current_lebesgue_measure = calculate_lebesgue_measure(pareto_front,max_search)

        improvements = []
        
        for k in range(len(vs_mean)):
            # Monte Carlo sampling to generate virtual samples
            y_samples = Monte_Carlo(vs_mean[k], vs_vars[k], times=times)
            
            # Compute the new Pareto front by adding y_sample to the original data
            improvement_sum = 0
            
            for y_sample in y_samples:
                extended_y = np.vstack([y, y_sample])
                new_pareto_front = get_pareto_front(extended_y,max_search)
                new_lebesgue_measure = calculate_lebesgue_measure(new_pareto_front,max_search)
                
                # Calculate the difference in Lebesgue measures
                improvement = new_lebesgue_measure - current_lebesgue_measure if max_search else current_lebesgue_measure - new_lebesgue_measure
                improvement_sum += max(improvement,0)
            
            # Average improvement over Monte Carlo samples
            avg_improvement = improvement_sum / times
            improvements.append(avg_improvement)

        # Return the index of the virtual sample with the highest expected improvement
        best_idx = np.argmax(improvements) if max_search else np.argmin(improvements)
    
    elif method == 'PI':
        # Calculate the current Pareto front based on the training targets
        pareto_front = get_pareto_front(y,max_search)
        current_lebesgue_measure = calculate_lebesgue_measure(pareto_front,max_search)

        improvements = []
        
        for k in range(len(vs_mean)):
            # Monte Carlo sampling to generate virtual samples
            y_samples = Monte_Carlo(vs_mean[k], vs_vars[k], times=times)
            
            # Compute the new Pareto front by adding y_sample to the original data
            improvement_sum = 0
            
            for y_sample in y_samples:
                extended_y = np.vstack([y, y_sample])
                new_pareto_front = get_pareto_front(extended_y,max_search)
                new_lebesgue_measure = calculate_lebesgue_measure(new_pareto_front,max_search)
                
                # Calculate the difference in Lebesgue measures
                improvement = new_lebesgue_measure - current_lebesgue_measure if max_search else current_lebesgue_measure - new_lebesgue_measure

                # count the nums for improvement 
                if improvement >0:
                    improvement_sum += 1
               
            # Average improvement over Monte Carlo samples
            avg_improvement = improvement_sum / times
            improvements.append(avg_improvement)
        # Return the index of the virtual sample with the highest expected improvement
        best_idx = np.argmax(improvements) if max_search else np.argmin(improvements)

        
    elif method == 'UCB':
        improvements= imp_ucb(vs_mean, vs_vars,y,max_search)
        best_idx = np.argmax(improvements)

    elif method == 'qNEHVI':
        # q-Noisy Expected Hypervolume Improvement
        # This method handles observation noise and supports batch acquisition (q > 1 points)

        # Estimate observation noise if not provided
        if noise_std is None:
            # Estimate noise from the variance in the training data
            # Use a simple heuristic: average standard deviation across objectives
            noise_std = np.mean(np.std(y, axis=0)) * 0.1  # Conservative estimate

        # For batch acquisition, we need to evaluate sets of points jointly
        if batch_size == 1:
            # Single point selection (similar to EHVI but with noise handling)
            improvements = []

            for k in range(len(vs_mean)):
                # Monte Carlo sampling to generate virtual samples
                # Sample both from predictive distribution AND observation noise
                improvement_sum = 0

                for _ in range(times):
                    # Sample from predictive distribution (model uncertainty)
                    y_sample_pred = Monte_Carlo(vs_mean[k], vs_vars[k], times=1)[0]

                    # Add observation noise
                    obs_noise = np.random.normal(0, noise_std, size=y_sample_pred.shape)
                    y_sample = y_sample_pred + obs_noise

                    # Also sample noisy versions of existing observations
                    # This accounts for the fact that observed points are noisy
                    y_noisy = y + np.random.normal(0, noise_std, size=y.shape)

                    # Compute Pareto front with noisy observations
                    pareto_front_current = get_pareto_front(y_noisy, max_search)
                    current_hv = calculate_lebesgue_measure(pareto_front_current, max_search)

                    # Compute new Pareto front with added point
                    extended_y = np.vstack([y_noisy, y_sample])
                    new_pareto_front = get_pareto_front(extended_y, max_search)
                    new_hv = calculate_lebesgue_measure(new_pareto_front, max_search)

                    # Calculate improvement
                    improvement = new_hv - current_hv if max_search else current_hv - new_hv
                    improvement_sum += max(improvement, 0)

                # Average improvement over Monte Carlo samples
                avg_improvement = improvement_sum / times
                improvements.append(avg_improvement)

            # Return the index with highest expected improvement
            best_idx = np.argmax(improvements)

        else:
            # Batch selection (q > 1 points)
            # Use a greedy sequential approach: select points one at a time
            # This is a practical approximation to full joint optimization
            selected_indices = []
            improvements = np.zeros(len(vs_mean))

            for q in range(batch_size):
                batch_improvements = []

                for k in range(len(vs_mean)):
                    if k in selected_indices:
                        # Skip already selected points
                        batch_improvements.append(-np.inf)
                        continue

                    # Evaluate adding this point to the current batch
                    improvement_sum = 0

                    for _ in range(times):
                        # Sample noisy observations
                        y_noisy = y + np.random.normal(0, noise_std, size=y.shape)

                        # Add previously selected points in this batch
                        current_y = y_noisy.copy()
                        for idx in selected_indices:
                            y_sample_pred = Monte_Carlo(vs_mean[idx], vs_vars[idx], times=1)[0]
                            obs_noise = np.random.normal(0, noise_std, size=y_sample_pred.shape)
                            y_sample = y_sample_pred + obs_noise
                            current_y = np.vstack([current_y, y_sample])

                        # Compute current hypervolume
                        pareto_front_current = get_pareto_front(current_y, max_search)
                        current_hv = calculate_lebesgue_measure(pareto_front_current, max_search)

                        # Add candidate point
                        y_sample_pred = Monte_Carlo(vs_mean[k], vs_vars[k], times=1)[0]
                        obs_noise = np.random.normal(0, noise_std, size=y_sample_pred.shape)
                        y_sample = y_sample_pred + obs_noise
                        extended_y = np.vstack([current_y, y_sample])

                        # Compute new hypervolume
                        new_pareto_front = get_pareto_front(extended_y, max_search)
                        new_hv = calculate_lebesgue_measure(new_pareto_front, max_search)

                        # Calculate improvement
                        improvement = new_hv - current_hv if max_search else current_hv - new_hv
                        improvement_sum += max(improvement, 0)

                    # Average improvement
                    avg_improvement = improvement_sum / times
                    batch_improvements.append(avg_improvement)

                # Select point with highest improvement for this batch position
                best_idx_q = np.argmax(batch_improvements)
                selected_indices.append(best_idx_q)
                improvements[best_idx_q] = batch_improvements[best_idx_q]

            # For batch mode, return the first selected index (for compatibility)
            # but store all selected indices in improvements array
            best_idx = selected_indices[0]
            # Mark selected indices with their improvement values
            for idx in selected_indices[1:]:
                improvements[idx] = batch_improvements[idx]

    return best_idx,improvements
