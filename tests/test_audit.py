"""Tests for the audit-script license-family detector."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from audit_repos import detect_license_family  # noqa: E402


class TestDetectLicenseFamily:
    def test_apache_2_0(self):
        text = """
                                 Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/

   TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION
        """
        spdx, is_prop = detect_license_family(text)
        assert spdx == "Apache-2.0"
        assert is_prop is False

    def test_gpl_3_0(self):
        text = """
                    GNU GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007

 Copyright (C) 2007 Free Software Foundation, Inc.
        """
        spdx, is_prop = detect_license_family(text)
        assert spdx == "GPL-3.0"
        assert is_prop is False

    def test_gpl_2_0(self):
        text = """
                    GNU GENERAL PUBLIC LICENSE
                       Version 2, June 1991
        """
        spdx, is_prop = detect_license_family(text)
        assert spdx == "GPL-2.0"
        assert is_prop is False

    def test_lgpl_3_0(self):
        text = """
                   GNU LESSER GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007
        """
        spdx, is_prop = detect_license_family(text)
        assert spdx == "LGPL-3.0"
        assert is_prop is False

    def test_mit(self):
        text = """MIT License

Copyright (c) 2026 Adam

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files...
        """
        spdx, is_prop = detect_license_family(text)
        assert spdx == "MIT"
        assert is_prop is False

    def test_mpl_2_0(self):
        text = """Mozilla Public License Version 2.0
==================================
        """
        spdx, is_prop = detect_license_family(text)
        assert spdx == "MPL-2.0"
        assert is_prop is False

    def test_bsd_3_clause(self):
        text = """BSD 3-Clause License

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:

1. Redistributions of source code must retain the above copyright notice...
2. Redistributions in binary form must reproduce the above copyright notice...
3. Neither the name of the copyright holder nor the names of its contributors...
        """
        spdx, is_prop = detect_license_family(text)
        assert spdx == "BSD-3-Clause"
        assert is_prop is False

    def test_bsd_2_clause(self):
        text = """BSD 2-Clause License

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

1. Redistributions of source code must retain the above copyright notice...
2. Redistributions in binary form must reproduce the above copyright notice...
        """
        spdx, is_prop = detect_license_family(text)
        assert spdx == "BSD-2-Clause"
        assert is_prop is False

    def test_unlicense(self):
        text = """This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software...
        """
        spdx, is_prop = detect_license_family(text)
        assert spdx == "Unlicense"
        assert is_prop is False


class TestProprietaryDetection:
    def test_proprietary_software_explicit(self):
        text = """Proprietary Software License

Copyright (c) 2026 Acme Corp. All rights reserved.

This software is proprietary and confidential.
        """
        spdx, is_prop = detect_license_family(text)
        assert spdx == "Proprietary"
        assert is_prop is True

    def test_all_rights_reserved_without_mit_template(self):
        text = """Copyright (c) 2026 Acme Corp.

All rights reserved. Unauthorized copying, distribution, or modification
of this code is strictly prohibited.
        """
        spdx, is_prop = detect_license_family(text)
        assert spdx == "Proprietary"
        assert is_prop is True

    def test_mit_with_all_rights_reserved_is_not_proprietary(self):
        """The MIT-style 'permission is hereby granted' clause overrides
        the boilerplate 'All rights reserved' copyright header."""
        text = """MIT License

Copyright (c) 2026 Adam Engelbrecht. All rights reserved.

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software...
        """
        spdx, is_prop = detect_license_family(text)
        assert spdx == "MIT"
        assert is_prop is False

    def test_apache_text_does_not_match_proprietary_heuristic(self):
        """Apache LICENSE doesn't say 'proprietary' anywhere — must not
        be misclassified."""
        text = """Apache License Version 2.0, January 2004

TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION
        """
        spdx, is_prop = detect_license_family(text)
        assert spdx == "Apache-2.0"
        assert is_prop is False

    def test_gpl_preamble_mentioning_proprietary_not_misclassified(self):
        """GPL-3.0 preamble talks about 'proprietary' programs while
        explaining what the GPL prevents. The detector must still
        identify the file as GPL-3.0, not Proprietary."""
        text = """                    GNU GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007

  The GNU General Public License is a free, copyleft license for
software and other kinds of works. ... make it effectively proprietary.
To prevent this, the GPL assures that the patent cannot be used to
render the program non-free. ... into proprietary programs.
        """
        spdx, is_prop = detect_license_family(text)
        assert spdx == "GPL-3.0"
        assert is_prop is False


class TestEdgeCases:
    def test_empty_text(self):
        spdx, is_prop = detect_license_family("")
        assert spdx is None
        assert is_prop is False

    def test_unrecognized_text(self):
        spdx, is_prop = detect_license_family("Some random text that isn't a license.")
        assert spdx is None
        assert is_prop is False

    def test_case_insensitive(self):
        text = "APACHE LICENSE VERSION 2.0"
        spdx, is_prop = detect_license_family(text)
        assert spdx == "Apache-2.0"
