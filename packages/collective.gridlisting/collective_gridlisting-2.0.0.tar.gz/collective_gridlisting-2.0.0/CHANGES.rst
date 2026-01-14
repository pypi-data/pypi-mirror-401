Changelog
=========

.. You should *NOT* be adding new change log entries to this file.
   You should create a file in the news directory instead.
   For helpful instructions, please see:
   https://github.com/plone/plone.releaser/blob/master/ADD-A-NEWS-ITEM.rst

.. towncrier release notes start

2.0.0 (2026-01-13)
------------------

Breaking changes:


- Native namespace package support only (drop support for Python <3.10 and Plone <6.1).
  @petschki


Internal:


- Update configuration files.
  [plone devs]


1.2.4 (2025-03-12)
------------------

- Fix non-required boolean field.
  [petschki]


1.2.3 (2025-03-11)
------------------

- Refactor default value lookup from adapter to `defaultFactory`.
  [petschki]


1.2.2 (2025-03-05)
------------------

- Fix IValue adapter to lookup only our behavior fields.
  [petschki]

- JS Dependency cleanup and upgrades.
  [petschki]


1.2.1 (2024-10-25)
------------------

- Dependency updates.
  [petschki]


1.2.0 (2024-07-02)
------------------

- Enable cropping for preview images.
  [petschki]


1.1.3 (2024-07-02)
------------------

- Fix value for ``preview_scale``.
  [petschki]


1.1.2 (2024-07-02)
------------------

- Fix default values for ``show_more_link`` and ``more_link_text``
  [petschki]


1.1.1 (2024-06-06)
------------------

- Fix ``missing_value`` for Choice Fields.
  [petschki]


1.1.0 (2024-06-04)
------------------

- Add controlpanel to define site-wide defaults.
  [petschki]


1.0.0 (2023-06-28)
------------------

- Initial release. See README.rst
  [petschki]
