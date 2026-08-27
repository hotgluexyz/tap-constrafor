from hotglue_smoke_test.vcr.tap import VCRTapTestRunner

from tap_constrafor.tap import TapConstrafor


class Runner(VCRTapTestRunner):

    PRESERVE_KEYS = {"id", "updated_at", "insurance_policy_id"}

    def module(self) -> str:
        return "tap_constrafor.tap"

    def launch(self):
        TapConstrafor.cli()


if __name__ == "__main__":
    Runner.main()
