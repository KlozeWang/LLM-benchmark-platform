import argparse

from evaluation.arguments import get_args
#from SwissArmyTransformer import get_args, get_tokenizer
#from SwissArmyTransformer.arguments import initialize_distributed
#from SwissArmyTransformer.model import GLM130B

def add_bminf_args(parser):
    """Arguments for BMInf"""
    group = parser.add_argument_group("BMInf")

    group.add_argument("--bminf", action="store_true", help="Use BMInf to support low resource evaluation")
    group.add_argument("--bminf-memory-limit", type=int, default=20, help="Max memory for model per GPU (in GB)")
    return parser


def add_quantization_args(parser):
    group = parser.add_argument_group("Quantization")

    group.add_argument("--quantization-bit-width", type=int, default=None)
    group.add_argument("--from-quantized-checkpoint", action="store_true", help="Loading from a quantized checkpoint")


def add_initialization_args(parser):
    group = parser.add_argument_group("Initialization")

    group.add_argument(
        "--sequential-initialization",
        action="store_true",
        help="Initialize sequentially in tensor parallel group (reduce CPU RAM for initialization)",
    )


def initialize(extra_args_provider):
    parser = argparse.ArgumentParser(add_help=False)
    add_bminf_args(parser)
    add_quantization_args(parser)
    add_initialization_args(parser)
    extra_args_provider(parser)
    known, args_list = parser.parse_known_args()
    args = get_args(args_list)
    args = argparse.Namespace(**vars(args), **vars(known))
    args.do_train = False
    return args


