# ForgeMind public alpha lab

A small public regression lab,not ForgeMind source or a production service.
The humanize package in vendor/ is copied unchanged from public MIT-licensed
upstream commit785e5dcc0d0308ad0dff3f6cc0faa7085ad0375b;see UPSTREAM.json and
UPSTREAM_LICENSE. A generated version label is the only packaging addition.

## Real issue
Upstream issue:https://github.com/python-humanize/humanize/issues/460
naturalsize ignores the active locale's decimal separator. For fr_FR/de_DE,
the existing i18n API reports a comma but the numeric value uses a period.
The alpha task is to repair only vendor/humanize/filesize.py while preserving
English output,binary/GNU suffixes,custom format strings and negative values.
No changes to tests,workflow,license,provenance or permissions are allowed.

## Baseline truth
Nine existing-behavior controls pass. Two locale acceptance cases intentionally
fail on this unmodified upstream snapshot. CI runs all11cases;the initial branch
is expected to be red until the real defect is fixed. Failures are not hidden.
Locale tests use a synthetic NullTranslations fixture so unbuilt .mo catalogs
cannot masquerade as the numeric-formatting bug. Actual locale activation and
decimal_separator functions are exercised. No private/customer data is used.

## Run
Use Python3.12 and pytest9.1.1 in an isolated environment:

    python -m pytest -q

## Pilot boundaries
One proposed bounded NVIDIA patch request,no paid fallback. Provider/resource
approval and independent ForgeMind review must pass before executing it.
A draftPR and its exact-head CI are required evidence;no automatic merge.
A public toy success or this real defect alone does not prove production safety.
This repository contains no ForgeMind implementation,credential,runtime state,
original recovered code or hidden evaluator fixture. No upstream issue/comment
or PR is created by this lab;it is not a claim of upstream acceptance.
