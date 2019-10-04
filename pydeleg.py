import os
import jinja2
from jinja2 import Template
from subprocess import call
from argparse import ArgumentParser
from pandas import Timestamp, Timedelta, to_datetime
from number_to_word import number_to_word

city_diets = {
    'Amsterdam': (50, 'EUR'),
    'Paryż': (50, 'EUR'),
    'Poznań': (30, 'PLN'),
}

latex_jinja_env = jinja2.Environment(
    block_start_string = '\BLOCK{',
    block_end_string = '}',
    variable_start_string = '\VAR{',
    variable_end_string = '}',
    comment_start_string = '\#{',
    comment_end_string = '}',
    line_statement_prefix = '%%',
    line_comment_prefix = '%#',
    trim_blocks = True,
    autoescape = False,
    loader = jinja2.FileSystemLoader(os.path.abspath('./templates'))
)

def create_simple_trips(rest_args, args):
    rest_args = dict(rest_args)
    args = dict(args)
    start_date = rest_args['startdate']
    end_date = rest_args['enddate']
    start = args['startcity']
    end = args['endcity']
    mean = rest_args['transportmean']
    trip_there = (start, start_date, args['dephour'], end, start_date, args['arrivalthere'], mean)
    trip_back = (end, end_date, args['backhour'], start, end_date, args['arrivalhere'], mean)
    return [trip_there, trip_back]


def get_params_from_file(fname):
    with open(fname, 'r') as f:
        lines = f.readlines()
    args = [(splitted[0], splitted[1].strip()) for line in lines for splitted in (line.split(': '),) if len(splitted) == 2]
    args_dict = dict(args)
    meals = {}
    meals['breakfasts'] = args_dict.get('breakfasts', 0)
    meals['lunches'] = args_dict.get('lunches', 0)
    meals['dinners'] = args_dict.get('dinners', 0)
    trip_args = []
    for i, (k, v) in enumerate(args):
        if k == 'trips':
            if v == 'simple':  # plane, one trip there one trip back, same day
                tmp_args = args[i+1:]
                trip_args = create_simple_trips(args[:i], tmp_args)
            else:
                trip_args = [x.split(' ') for x in args[i+1:]]
            args = args[:i]
            break
    else:
        raise ValueError("No trips found.")
    return dict(args), trip_args, meals


def calc_diets(trip_args, breakfasts=0, lunches=0, dinners=0):
    city = trip_args[0][-4]
    start_datetime = to_datetime(f'{trip_args[0][1]} {trip_args[0][2]}', dayfirst=True)
    end_datetime = to_datetime(f'{trip_args[-1][-3]} {trip_args[-1][-2]}', dayfirst=True)
    perdiem, cur = city_diets[city]
    period = end_datetime - start_datetime
    full_days = period.days
    rest = period - Timedelta(days=full_days)
    diets = perdiem * full_days
    domestic = cur.lower() == 'pln'
    if not domestic:
        if rest.components.hours <= 8:
            diets += 0.33333 * perdiem
        elif 8 < rest.components.hours <= 12:
            diets += 0.5 * perdiem
        else:
            diets += perdiem

        diets -= 0.15 * perdiem * breakfasts
        diets -= 0.3 * perdiem * lunches
        diets -= 0.3 * perdiem * dinners
    else:  # domestic
        if rest.components.hours <= 8:
            diets += 0.5 * perdiem
        else:
            diets += perdiem

        diets -= 0.25 * perdiem * breakfasts
        diets -= 0.5 * perdiem * lunches
        diets -= 0.25 * perdiem * dinners
    return diets, cur


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--file', type=str, required=True)
    args = parser.parse_args()
    fname = args.file
    args, trips, meals = get_params_from_file(fname)
    dietval, dietcur = calc_diets(trips, **meals)
    dietvalword = number_to_word(dietval, dietcur)
    params = {
        'dietval': f'{dietval:0.2f}',
        'dietcur': dietcur,
        'dietvalword': dietvalword,
        'trips': trips,
        **args
    }
    s = latex_jinja_env.get_template('./del-temp.tex').render(params)
    base, _ = os.path.splitext(os.path.basename(fname))
    path = f'/tmp/{base}.tex'
    with open(path, 'w') as f:
        f.write(s)
    call(['pdflatex', '-output-directory=./outputs', path])
    call(['rm', '-rf', f'./outputs/{base}.log', f'./outputs/{base}.aux'])
