---
title: "LocalBiz AI: A Local-First Marketing Assistant for Small Businesses"
published: false
tags: devchallenge, hf26challenge
---

*This is a submission for the [Hacktoberfest Open-Source AI Challenge Week 2: Side Hustle](https://dev.to/challenges/hacktoberfest-week2-2026-10-12)*

## What I Built

LocalBiz AI turns a few product details into an Instagram caption, WhatsApp message, product description, hashtags, and a call to action. It is aimed at small business owners who need affordable, quick marketing copy without hiring a dedicated marketer.

## Demo

<!-- Add a deployed demo link or short screen recording after testing. -->

## Code

<!-- Add your public GitHub repository URL here. -->

## How I Built It

The frontend uses HTML, CSS, and JavaScript. A FastAPI backend sends structured prompts to Gemma through Ollama for local open-weight inference. SQLite stores the content history on the same machine. An explicitly labelled template fallback keeps the workflow testable when Ollama is not installed or running.

## Why Does Open Innovation Matter?

Local inference can keep prompts on a business owner's own computer, avoid per-request cloud LLM API charges, and let developers experiment with different compatible models. The trade-off is that local inference uses the user's hardware and output quality depends on the model. The offline template fallback is not represented as AI output.

## My First User

<!-- Only complete this section after a real person tries it. Include what they asked for and whether they would pay. Do not invent feedback. -->

## Prize Categories

<!-- List only categories whose requirements your tested project actually meets. -->
