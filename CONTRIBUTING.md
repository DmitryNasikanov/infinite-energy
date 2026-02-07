# Contributing to Project Helios

Thank you for your interest in contributing! Project Helios is an open engineering roadmap for building a Dyson Swarm from Mercury, and we welcome contributions from anyone.

All content in this repository is licensed under [CC BY-SA 4.0](LICENSE).

## Types of Contributions

- **Text corrections** — typos, grammar, unclear wording
- **Scientific corrections** — errors in calculations, outdated data, missing references
- **Translations** — improving English translations or adding new languages
- **New content** — new calculations, analyses, or detailed topics
- **Website improvements** — CSS, navigation, Quarto configuration

## How to Contribute

1. **Fork** the repository
2. **Create a branch** for your changes (`git checkout -b fix/mre-calculation`)
3. **Make your changes** in the appropriate files
4. **Test locally** — install [Quarto](https://quarto.org/) and run `quarto render` to verify the site builds correctly
5. **Submit a pull request** with a clear description of your changes

## Project Structure

```
ru/              — Russian content (primary language)
  book/          — Science fiction novel
  science/       — Scientific documentation
    summaries/   — Overview articles
    detailed/    — In-depth technical articles
    reference/   — Glossary, constants, risks
en/              — English translations (science section)
  science/       — Mirrors ru/science/ structure
```

## Guidelines

- **Scientific accuracy** — cite sources for claims and calculations. Prefer peer-reviewed papers and established references.
- **International perspective** — this is a global project. Refer to "international launcher fleet" rather than specific national vehicles. Include examples from multiple space agencies (NASA, ESA, CNSA, Roscosmos, ISRO, JAXA).
- **Keep both languages in sync** — if you change content in `ru/`, the corresponding `en/` file should be updated too (or flag it in your PR for someone else to translate).
- **Quarto format** — content is written in `.qmd` files (Quarto Markdown). Follow existing formatting patterns.

## Getting Help

If you have questions or want to discuss ideas before submitting a PR, open a [Discussion](https://github.com/DmitryNasikanov/infinite-energy/discussions).
