from django.shortcuts import render

from gocal.web.forms import ExpressionForm
from gocal.web.utils import evaluate_expression, EvaluateExpressionError


def calculate(request):
    if request.method == 'POST':
        form = ExpressionForm(request.POST)
        if form.is_valid():
            expression = form.cleaned_data['user_input']
            ctx = {
                'form': form,
            }
            try:
                result = evaluate_expression(expression)
            # If invalid expression then raise the error
            except EvaluateExpressionError as e:
                ctx.update({
                    'error_message': e.message,
                    'status': 'FAILED',
                })
            else:
                ctx.update({
                    'expression': expression,
                    'status': 'SUCCESS',
                    'result': result,
                })
        # If form is not valid, render with errors
        # TODO: move expression validation to form level
        else:
            ctx = {
                'form': form,
                'status': 'FAILED',
                'error_message': 'Invalid Expression.'
            }
    # If it's not a POST request then only render the form
    else:
        form = ExpressionForm()
        ctx = {'form': form}

    return render(request, 'calculate.html', ctx)
