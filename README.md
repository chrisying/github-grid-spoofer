# GitHub Contributions Spoofer

This script will put a bunch of fake commits into THIS repo which will draw a
message on your GitHub contributions grid.

## Assumptions

* Grid is at least 52 weeks wide and 7 days tall
* Each column starts on Sunday and ends on Saturday
* Timezone depends on local time, if the viewer is >12 hours difference, the
  message may look offset or wrong

## How to customize for your usage

WARNING: I take no responsibility for any problems that may arise.

1. Fork this repo into your own GitHub account.
2. Clone onto your machine which has GitHub SSH key set up.
3. Modify the code in `github_grid_spoofer.py`: change `GITHUB_REPO` and any other constants you want.
4. Run `python3 github_grid_spoofer.py` (recommend dryrunning once).
5. If everything ran successfully, push the changes via `git push -f origin HEAD`.

GitHub usually takes a few minutes or so to fully update the contributions
grid, though according to the
[FAQ](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/managing-contribution-settings-on-your-profile/why-are-my-contributions-not-showing-up-on-my-profile#commit-was-made-less-than-24-hours-ago)
it can take up to 24 hours. From trial and error, it seems that if you push
multiple times, the previous contributions may not disappear immediately.
