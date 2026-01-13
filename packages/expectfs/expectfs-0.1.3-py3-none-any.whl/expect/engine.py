from expect.report import ValidationReport


def run_validation(context):
    report = ValidationReport()

    for target, rule in context.checks:
        ok, message = rule(target)
        if not ok:
            report.add_error(
                target=str(target),
                rule=rule.__name__,
                message=message,
            )

    return report
