#!/usr/bin/python
# -*- coding:Utf-8 -*-
#
#  Copyright (C) 2010 Mathieu Comandon <strider@strycore.com>
# 
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License version 3 as
#  published by the Free Software Foundation.
# 
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
# 
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 

import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lutris.gconfwrapper import GconfWrapper


class TestGConfWrapper(unittest.TestCase):
    def __init__(self):
        self.gconf = GconfWrapper()

    def runTest(self):
        self.assertEqual(self.gconf.has_key('/apps/metacity/general/button_layout'), True)
        self.assertEqual(self.gconf.has_key('/apps/metacity/general/bouton_disposition'), False)
        self.assertEqual(self.gconf.has_key('/foo/bar'), False)

        self.assertEqual(self.gconf.get_key('/foo/bar'), None)
        self.assertEqual(self.gconf.get_key('/apps/metacity/general/raise_on_click'), True)
        self.assertTrue(self.gconf.set_key('/apps/metacity/general/auto_raise_delay', 500, override_type = True))
        self.assertEqual(self.gconf.get_key('/apps/metacity/general/auto_raise_delay'), 500)

        self.assertTrue(self.gconf.set_key('/apps/metacity/general/raise_on_click', False))
        self.assertEqual(self.gconf.get_key('/apps/metacity/general/raise_on_click'), False)
        self.assertTrue(self.gconf.set_key('/apps/metacity/general/raise_on_click', True))
        self.assertEqual(self.gconf.get_key('/apps/metacity/general/raise_on_click'), True)

        self.assertTrue(self.gconf.set_key('/apps/metacity/general/auto_raise_delay', 499))
        self.assertEqual(self.gconf.get_key('/apps/metacity/general/auto_raise_delay'), 499)
        self.assertFalse(self.gconf.set_key('/apps/metacity/general/auto_raise_delay', "Five hundred"))
        self.assertTrue(self.gconf.set_key('/apps/metacity/general/auto_raise_delay', 500))

        print 'testing new keys'
        self.assertTrue(self.gconf.set_key('/apps/lutris/tests/foo', "dressed like pazuzu", override_type = True))
        self.assertEqual(self.gconf.get_key('/apps/lutris/tests/foo'), "dressed like pazuzu")
        self.assertEqual(self.gconf.all_dirs('/apps/lutris'), ['tests'])

if __name__ == '__main__':
    test = TestGConfWrapper()
    test.runTest()
