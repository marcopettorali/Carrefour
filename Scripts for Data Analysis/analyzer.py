import omnetpp_parser
import stats_util


def analyze_repetition(repetition_name):
    lists = omnetpp_parser.parse_vector_file(repetition_name + ".vec")
    response_time_list = lists[0]
    wait_time_list = lists[1]

    # response_time_results and wait_time_results contain the analysis results
    # of this repetition related to the two metrics
    response_time_results = []
    wait_time_results = []

    # *_results[0] : sample mean value
    response_time_results.append(stats_util.s_mean_value(response_time_list))
    wait_time_results.append(stats_util.s_mean_value(wait_time_list))

    # *_results[1] : sample lorenz curve gap
    response_time_results.append(stats_util.s_lorenz_curve_gap(response_time_list))
    wait_time_results.append(stats_util.s_lorenz_curve_gap(wait_time_list))

    # *_results[2] : sample median
    response_time_results.append(stats_util.s_percentile(response_time_list, 0.5))
    wait_time_results.append(stats_util.s_percentile(wait_time_list, 0.5))

    # *_results[3] : sample first quartile
    response_time_results.append(stats_util.s_percentile(response_time_list, 0.25))
    wait_time_results.append(stats_util.s_percentile(wait_time_list, 0.25))

    # *_results[4] : sample third quartile
    response_time_results.append(stats_util.s_percentile(response_time_list, 0.75))
    wait_time_results.append(stats_util.s_percentile(wait_time_list, 0.75))

    # *_results[5] : sample 98th percentile
    response_time_results.append(stats_util.s_percentile(response_time_list, 0.98))
    wait_time_results.append(stats_util.s_percentile(wait_time_list, 0.98))

    # let's read the time average number of customers in this repetition from the .sca file
    timeavg_num_customers = omnetpp_parser.parse_scalar_file(repetition_name + ".sca")

    # return the elaborated values for this repetition
    return [response_time_results, wait_time_results, timeavg_num_customers]


def analyze_scenario(scenario_name):

    # lists collecting the values for each performance indicator for response time metric
    r_t_mean_samples = []
    r_t_lcg_samples = []
    r_t_0_5_samples = []
    r_t_0_25_samples = []
    r_t_0_75_samples = []
    r_t_0_98_samples = []

    # lists collecting the values for each performance indicator for wait time metric
    w_t_mean_samples = []
    w_t_lcg_samples = []
    w_t_0_5_samples = []
    w_t_0_25_samples = []
    w_t_0_75_samples = []
    w_t_0_98_samples = []

    # list collecting the values for each performance indicator for number of customers metric
    n_c_mean_samples = []

    for repetition_number in range(0, 35):
        # analyze this repetition
        lists = analyze_repetition(scenario_name + "-#" + str(repetition_number))

        # filling the lists with the correct values
        r_t_mean_samples.append(lists[0][0])
        r_t_lcg_samples.append(lists[0][1])
        r_t_0_5_samples.append(lists[0][2])
        r_t_0_25_samples.append(lists[0][3])
        r_t_0_75_samples.append(lists[0][4])
        r_t_0_98_samples.append(lists[0][5])
        w_t_mean_samples.append(lists[1][0])
        w_t_lcg_samples.append(lists[1][1])
        w_t_0_5_samples.append(lists[1][2])
        w_t_0_25_samples.append(lists[1][3])
        w_t_0_75_samples.append(lists[1][4])
        w_t_0_98_samples.append(lists[1][5])
        n_c_mean_samples.append(lists[2])

    # let's put all the lists into a single list, to iterate through them
    samples_lists = [r_t_mean_samples, r_t_lcg_samples, r_t_0_5_samples, r_t_0_25_samples, r_t_0_75_samples,
                     r_t_0_98_samples, w_t_mean_samples, w_t_lcg_samples, w_t_0_5_samples, w_t_0_25_samples,
                     w_t_0_75_samples, w_t_0_98_samples, n_c_mean_samples]

    # let's create the list containing all the confidence intervals for each performance index of each metric
    # confidence_intervals[0] = C.I. for the mean value of the sample mean value of the response time (one per repetition)
    # confidence_intervals[1] = C.I. for the mean value of the sample lorenz curve gap of the response time (one per repetition)
    # confidence_intervals[2] = C.I. for the mean value of the sample median of the response time (one per repetition)
    # confidence_intervals[3] = C.I. for the mean value of the sample 1st quartile of the response time (one per repetition)
    # confidence_intervals[4] = C.I. for the mean value of the sample 3rd quartile of the response time (one per repetition)
    # confidence_intervals[5] = C.I. for the mean value of the sample 98th percentile of the response time (one per repetition)
    # confidence_intervals[6] = C.I. for the mean value of the sample mean value of the wait time (one per repetition)
    # confidence_intervals[7] = C.I. for the mean value of the sample lorenz curve gap of the wait time (one per repetition)
    # confidence_intervals[8] = C.I. for the mean value of the sample median of the wait time (one per repetition)
    # confidence_intervals[9] = C.I. for the mean value of the sample 1st quartile of the wait time (one per repetition)
    # confidence_intervals[10] = C.I. for the mean value of the sample 3rd quartile of the wait time (one per repetition)
    # confidence_intervals[11] = C.I. for the mean value of the sample 98th percentile of the wait time (one per repetition)
    # confidence_intervals[12] = C.I. for the mean value of the sample mean value of the number of customers (one per repetition)

    confidence_intervals = []

    for samples in samples_lists:
        # calculate C.I. for each sample list
        confidence_intervals.append(stats_util.s_mean_confidence_interval(samples))

    # plot correlograms
    stats_util.plot_correlogram(r_t_mean_samples, scenario_name, "Response Time - Mean Values")
    stats_util.plot_correlogram(r_t_lcg_samples,scenario_name, "Response Time - Lorenz Curve Gaps")
    stats_util.plot_correlogram(r_t_0_5_samples,scenario_name, "Response Time - Medians")
    stats_util.plot_correlogram(r_t_0_25_samples,scenario_name, "Response Time - First Quartiles")
    stats_util.plot_correlogram(r_t_0_75_samples,scenario_name, "Response Time - Third Quartiles")
    stats_util.plot_correlogram(r_t_0_98_samples,scenario_name, "Response Time - 98th Percentiles")

    stats_util.plot_correlogram(w_t_mean_samples,scenario_name, "Wait Time - Mean Values")
    stats_util.plot_correlogram(w_t_lcg_samples,scenario_name, "Wait Time - Lorenz Curve Gaps")
    stats_util.plot_correlogram(w_t_0_5_samples,scenario_name, "Wait Time - Medians")
    stats_util.plot_correlogram(w_t_0_25_samples,scenario_name, "Wait Time - First Quartiles")
    stats_util.plot_correlogram(w_t_0_75_samples,scenario_name, "Wait Time - Third Quartiles")
    stats_util.plot_correlogram(w_t_0_98_samples,scenario_name, "Wait Time - 98th Percentiles")

    stats_util.plot_correlogram(n_c_mean_samples,scenario_name, "Num of Customers - Mean Values")

    return confidence_intervals
