from phase3_enrich2 import run_phase_3
from phase2_filter2 import run_phase_2
from phase4_score import run_phase_4


def run_pipeline():
    print(" STARTING FULL PIPELINE\n")

    run_phase_3()
    print("\n Phase 3 Done\n")

    run_phase_2()
    print("\n Phase 2 Done\n")

    run_phase_4()
    print("\n Phase 4 Done\n")

    print(" PIPELINE COMPLETE")


if __name__ == "__main__":
    run_pipeline()
