# Contribution Workflow

Workflow proposed by the lecturer in the DSPRO1 course information. Follow it for every deliverable.

## Ground rules

- `main` always reflects the current state of development — **do not commit directly to `main`** (except merging PRs during coaching).
- Every deliverable gets its own branch + Pull Request.
- The commit history must show that **all team members** contributed (unbalanced histories affect individual grading).
- Coaches are always added as **reviewers**.
- Coaches GitHub usernames: `curdon`, `lnazarenko`, `dmousadakos`.

## Steps

1. Clone the repository locally (once).
2. Create a new branch from `main` when starting a new deliverable:

   ```
   git checkout main
   git pull
   git checkout -b dlv<number>-<short-topic>
   ```

   Examples: `dlv1-topic-pitch`, `dlv3-data-sources-eda`.
3. Work on the branch. Teammates may create per-user sub-branches (`dlv<number>-<user>-<topic>`).
4. Commit often with clear messages; push the branch.
5. When the deliverable is due and complete, open a **Pull Request into `main`** and request review from all coaches.
6. PRs are reviewed and merged into `main` during the coaching session.

## Branch naming

| Prefix | Use |
|---|---|
| `dlv<N>-<topic>` | Deliverable work (N = 1..6) |
| `dlv<N>-<user>-<topic>` | Per-user sub-branch within a deliverable |
| `fix-<topic>` | Small fixes |

## Deliverable → CRISP-DM mapping

| Deliverable | CRISP-DM phase | README section |
|---|---|---|
| 1 Project Title & Pitch | Business Understanding | Project Details / 1 |
| 2 Problem Statement & Goals | Business Understanding | 1 |
| 3 Data Sources & EDA | Data Understanding | 2 |
| 4 Data Modelling | Data Modeling | 3–4 |
| 5 Evaluation | Evaluation | 5 |
| 6 SDG | cross-cutting | 6 |

## Do not commit

- Raw/large data (see `.gitignore`) — document download links instead.
- Secrets, API tokens, `.env`.
