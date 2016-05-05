#!/usr/bin/python
# coding=utf-8
from sklearn.metrics import explained_variance_score
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import median_absolute_error
from sklearn.metrics import r2_score
from terminaltables import AsciiTable as Table

# TODO: Verteilung der FEhler
# TODO: Beispiele Versionen (als liste übergeben oder so)
# TODO: Score im Verhältnis zu z.B. Alter der Files setzen oder zum Alter des Repos

SCORE_EVS = "evs"  # Explained Variance Score
SCORE_MSE = "mse"  # Mean Equared Error
SCORE_MAE = "mae"  # Mean Absolute Error
SCORE_MDE = "mde"  # MeDian absolute Error
SCORE_R2S = "r2s"  # R^2 Score


class Report:
    def __init__(self, ground_truth, predicted, label=""):
        self.ground_truth = ground_truth
        self.predicted = predicted
        self.label = label
        self.evs = None
        self.mse = None
        self.mae = None
        self.mde = None
        self.r2s = None

        self.update()

    def update(self):
        self.evs = get_explained_variance_score(self.ground_truth, self.predicted)
        self.mse = get_mean_squared_error(self.ground_truth, self.predicted)
        self.mae = get_mean_absolute_error(self.ground_truth, self.predicted)
        self.mde = get_median_absolute_error(self.ground_truth, self.predicted)
        self.r2s = get_r2_score(self.ground_truth, self.predicted)

    def __str__(self):
        output_data = [
            ["Value", "Description", "Info"]
        ]

        if self.evs is not None:
            output_data.append([_format_float(self.evs), "Explained variance score", "Best is 1.0, lower is worse"])
        if self.mse is not None:
            output_data.append([_format_float(self.mse), "Mean squared error", "Best is 0.0, higher is worse"])
        if self.mae is not None:
            output_data.append([_format_float(self.mae), "Mean absolute error", "Best is 0.0, higher is worse"])
        if self.mde is not None:
            output_data.append([_format_float(self.mde), "Median absolute error", "Best is 0.0, higher is worse"])
        if self.r2s is not None:
            output_data.append([_format_float(self.r2s), "R2 Score", "Best is 1.0, lower is worse"])
        table = Table(output_data)
        table.title = "Report"
        if self.label:
            table.title += ": " + self.label
        return table.table


def _score_attr_to_string(score_attr):
    if score_attr == SCORE_EVS:
        return "Explained variance score"
    elif score_attr == SCORE_MSE:
        return "Mean squared error"
    elif score_attr == SCORE_MAE:
        return "Mean absolute error"
    elif score_attr == SCORE_MDE:
        return "Median absolute error"
    elif score_attr == SCORE_R2S:
        return "R2 Score"


def _format_float(float_value):
    return "% .4f" % float_value


def get_report_comparisation_table(reports, score_attr):
    compare_table = [
        [report.label for report in reports],
        [_format_float(getattr(report, score_attr)) for report in reports]
    ]
    table = Table(compare_table)
    table.title = _score_attr_to_string(score_attr) + " comparisation"


def get_metrics(ground_truth, predicted):
    """ Calculate all metrics at once.

    Args:
        ground_truth (ndarray): The ground truth target array.
        predicted (ndarray): The predicted target array.

    Returns:
        tuple: The different linear regression metrics.
    """
    return (
        get_explained_variance_score(ground_truth, predicted),
        get_mean_squared_error(ground_truth, predicted),
        get_mean_absolute_error(ground_truth, predicted),
        get_median_absolute_error(ground_truth, predicted),
        get_r2_score(ground_truth, predicted),
    )


def get_explained_variance_score(ground_truth, predicted):
    """ Calculates the explained variance.

    The explained variance is a measure of how well the model can explain the variance of the ground truth.
    The best possible result is 1, lower ist worse.

    Args:
        ground_truth (ndarray): The ground truth target array.
        predicted (ndarray): The predicted target array.

    Returns:
        float: The calculated value.
    """
    return explained_variance_score(ground_truth, predicted)


def get_mean_squared_error(ground_truth, predicted):
    """ Calculates the mean squared error.

    This score represents the mean of the squared residuals between the ground truth and predicted values.
    In short: MSE = mean((ground-truth - predicted)^2)
    The best possible result is 0, higher is worse.

    Args:
        ground_truth (ndarray): The ground truth target array.
        predicted (ndarray): The predicted target array.

    Returns:
        float: The calculated value.
    """
    return mean_squared_error(ground_truth, predicted)


def get_mean_absolute_error(ground_truth, predicted):
    """ Calculates the mean absolute error

    This score represents the mean of the absolute residuals between ground truth and predicted values.
    In short: MAE = mean(|ground-truth - predicted|)
    The best possible result is 0, higher is worse.

    Args:
        ground_truth (ndarray): The ground truth target array.
        predicted (ndarray): The predicted target array.

    Returns:
        float: The calculated value.
    """
    return mean_absolute_error(ground_truth, predicted)


def get_median_absolute_error(ground_truth, predicted):
    """ Calculates the median absolute error

    This score represents the median of the absolute residuals between ground truth and predicted values.
    In short: MAE = median(|ground-truth[0] - predicted[0]|, ..., |ground-truth[n] - predicted[n]|)
    The best possible result is 0, higher is worse.

    Args:
        ground_truth (ndarray): The ground truth target array.
        predicted (ndarray): The predicted target array.

    Returns:
        float: The calculated value.
    """
    return median_absolute_error(ground_truth, predicted)


def get_r2_score(ground_truth, predicted):
    """ Calculates the R^2 score (a.k.a. Coefficient of determination)

    This score represents the quality of the prediction by how much it explains the ground truths variance.
    The best possible result is 1, lower is worse.

    Args:
        ground_truth (ndarray): The ground truth target array.
        predicted (ndarray): The predicted target array.

    Returns:
        float: The calculated value.
    """
    return r2_score(ground_truth, predicted)
