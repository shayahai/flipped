# Flipped by AMKAR

Renovation planner and quoting tool for Bathroom Flip / AMKAR Building Group.

The live planner is at https://shayahai.github.io/flipped/ and asks for an
access code before it opens.

## How it is put together

- The `gh-pages` branch is the website that GitHub Pages serves.
- The planner is one HTML page. It is not kept in this repository in readable
  form: the website holds it encrypted, and the access code is the key.
- `tools/build.py` makes the website page from the planner page:

      FLIPPED_CODE=<access code> python3 tools/build.py planner.html site/

  It writes `index.html` (the access-code page with the encrypted planner
  inside) and `sw.js` (keeps the planner opening with no reception). The other
  site files (`manifest.webmanifest`, the icons from `tools/mkicon.py`, and
  `pdf-lib.min.js` 1.17.1 for PDF export) sit beside them.

Never commit the readable planner page or the access code.
