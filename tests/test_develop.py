import sys
import unittest

import uasyncio as asyncio
import umock

sys.path.insert(0, "../src")
import henri.develop  # isort:skip


class TestDevelop(unittest.TestCase):
    def test_create_agitate_list(self):
        resp = umock.AsyncTestRunner().run(henri.develop.create_agitate_list(180, 60))
        self.assertEqual(
            resp,
            [
                179,
                178,
                177,
                176,
                175,
                174,
                173,
                172,
                171,
                170,
                169,
                168,
                167,
                166,
                165,
                164,
                163,
                162,
                161,
                160,
                159,
                158,
                157,
                156,
                155,
                154,
                153,
                152,
                151,
                150,
                149,
                148,
                147,
                146,
                145,
                144,
                143,
                142,
                141,
                140,
                139,
                138,
                137,
                136,
                135,
                134,
                133,
                132,
                131,
                130,
                129,
                128,
                127,
                126,
                125,
                124,
                123,
                122,
                121,
                120,
                59,
                58,
                57,
                56,
                55,
                54,
                53,
                52,
                51,
                50,
            ],
        )

    def test_process(self):
        mock_agitate = umock.AsyncMock()
        mock_sleep = umock.AsyncMock()

        with umock.MonkeyPatch(henri.develop, "agitate", mock_agitate):
            with umock.MonkeyPatch(asyncio, "sleep", mock_sleep):
                umock.AsyncTestRunner().run(
                    henri.develop.process(60, [50, 40, 30, 20, 10])
                )

        self.assertEqual(len(mock_agitate.call_args_list), 5)
        self.assertEqual(len(mock_sleep.call_args_list), 55)
