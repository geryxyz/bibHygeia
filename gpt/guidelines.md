# Guidelines

## Entries' keys

Use the title's kebab-case version to form the entry's key. Replace any non-English letters and non-numbers from the title with a dash (-) to form the key.

```bibtex
@article{the-true-meaning-of-42,
	author = {Walther Wombat and Klaus Koala},
	title = {The true meaning of 42},
	journal = {Journal of modern skepticism},
	date = {2016},
	keywords = {trusted},
}
```

If necessary, add the list of the kebab-case versions of authors' names to the end of the key to ensure their uniqueness.

```bibtex
@article{the-true-meaning-of-42-gerg--balogh,
	author = {Gergő Balogh},
	title = {The true meaning of 42},
	journal = {Journal of ancient skepticism},
	date = {1016},
	keywords = {trusted},
}

@article{the-true-meaning-of-42-walther-wombat-klaus-koala,
	author = {Walther Wombat and Klaus Koala},
	title = {The true meaning of 42},
	journal = {Journal of modern skepticism},
	date = {2016},
	keywords = {trusted},
}
```

Why? Most of us use LaTeX editors, which offer smart completion of the BibTeX keys. It means we do not have to type the long full keys. The cited entry will be more evident for all authors since the title is a human-readable descriptor.
