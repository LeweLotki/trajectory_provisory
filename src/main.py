from config import paths

from argparse import ArgumentParser

from os import listdir
from os.path import basename

def main():

    program_description = get_description(path=paths.description_path)
    
    data_analysis_description = get_description(path=paths.data_analysis_description_path)

    parser = ArgumentParser(description=program_description)
    
    parser.add_argument('-a', '--notebook', help=data_analysis_description + f' {", ".join(available_notebooks)}')
    
    parser.add_argument('-e', action='store_true', help=data_extraction_description)

    args = parser.parse_args()
    
    if args.notebook: run_analysis(args.notebook)
    elif args.e: run_extraction()
    elif args.p: 
        if args.sampling_coef:
            cost_function(sampling_coef=args.sampling_coef)
        else: cost_function()
    elif args.s: 
        pso = PSO(
            file_path=args.cost_function_file_path,
            options=args.weights,
            n_particles=args.n_particles,
            iters=args.iters
        )
        pso.train()
        pso.display(fps=10)
    else: default_message()

def default_message():
    
    print("\r No option specified. \n\r Type '--help' for list of arguments.")

def get_description(path: str) -> str:
    
    with open(path, 'r', encoding='utf-8') as file:
        description = file.read().strip()
        return description
 
if __name__ == '__main__': main()
