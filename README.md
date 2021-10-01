# bibHygeia

## Elevator Pitch

Our researchers prefer to use LaTeX to prepare their scientific publications. But a good paper contains several citations to specify the context of the research. In the case of the LaTeX ecosystem, these references are stored in a centralized BibTeX database, which is embodied by one or more BIB files. In essence, these are source code files of the database. For example:

```
...

@Book{abramowitz+stegun,
 author    = "Milton {Abramowitz} and Irene A. {Stegun}",
 title     = "Handbook of Mathematical Functions with
              Formulas, Graphs, and Mathematical Tables",
 publisher = "Dover",
 year      =  1964,
 address   = "New York City",
 edition   = "ninth Dover printing, tenth GPO printing"
}

...
```

During the research, scientists may expand, change or reuse the list of these references. Hence they have to modify the underlying structure of these BIB files. Since researchers rarely work alone, the team members may use different styles when editing those files. This situation could lead to several so-called rule violations, like inconsistent style, duplicated entries, missing mandatory properties. These could reduce the quality of the paper under development and increase the time required to apply further changes in the bibliography database.

This project aims to provide an early detection system and possible suggestions for correcting the detected violations. We plan to integrate into the well-known project management systems, like GitHub and GitLab, hence checking the specified rules immediately after the changes were published (pushed).
