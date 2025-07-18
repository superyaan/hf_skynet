import sys
from utils.logger import get_logger
from utils.cli import parse_args, apply_overrides
from utils.config_loader import load_config
from utils.summary_manager import send_weekly_summary
from core.app import run_scan_cycle

logger = get_logger(__name__)

def main():
    args = parse_args()
    config = apply_overrides(load_config(), args)

    # Weekly summary mode
    if args.weekly_summary:
        send_weekly_summary(config)
        return

    # Normal scan cycle (scan -> report -> alerts -> summary update)
    run_scan_cycle(config)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.exception(f"Fatal error: {e}")
        sys.exit(1)