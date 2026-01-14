#  Copyright (c) 2024 Ubiterra Corporation. All rights reserved.
#  #
#  This ZoneVu Python SDK software is the property of Ubiterra Corporation.
#  You shall use it only in accordance with the terms of the ZoneVu Service Agreement.
#  #
#  This software is made available on PyPI for download and use. However, it is NOT open source.
#  Unauthorized copying, modification, or distribution of this software is strictly prohibited.
#  #
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
#  PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
#  FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
#  ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
#
#
#
#
#

"""
Well log service.

List and retrieve well logs for a wellbore, and optionally load curve samples
for each log and curve.
"""

import numpy as np
from ..datamodels.wells.Welllog import Welllog
from ..datamodels.wells.Wellbore import Wellbore
from ..datamodels.wells.Curve import Curve
from ..datamodels.wells.CurveGroup import CurveGroup
from .Client import Client
from typing import Optional


class WelllogService:
    """List, fetch, add, and transfer data for well logs and curves."""
    client: Client

    def __init__(self, c: Client):
        self.client = c

    def get_welllogs(self, wellboreId: int) -> list[Welllog]:
        """
        Get list of well logs for a wellbore.

        :param wellboreId: System ID of the wellbore.
        :return: List of Welllog objects (basic data). Curve samples are not loaded. Use load_welllogs to populate curves.
        :raises ZonevuError: If wellbore not found or network error occurs.
        """
        url = "welllogs/%s" % wellboreId
        items = self.client.get_list(url)
        logs = [Welllog.from_dict(w) for w in items]
        return logs

    def load_welllogs(self, wellbore: Wellbore, load_curves: bool = False) -> list[Welllog]:
        """
        Load well logs for a wellbore and optionally load curve samples.

        :param wellbore: Wellbore object to populate with logs (modified in-place).
        :param load_curves: If True, load curve sample data for each curve. If False (default), only load log metadata.
        :return: List of Welllog objects attached to the wellbore.
        :note: Setting load_curves=True will require additional API calls for each curve; use only if needed.
        """
        logs = self.get_welllogs(wellbore.id)
        wellbore.welllogs = logs

        if load_curves:
            for log in logs:
                for curve in log.curves:
                    self.load_curve_samples(curve)

        return logs

    def get_welllog(self, welllog_id: int) -> Welllog:
        """
        Get a single well log by its system ID.

        :param welllog_id: Welllog system ID.
        :return: Welllog object with metadata. Curve samples may not be loaded.
        :raises ZonevuError: If welllog not found or network error occurs.
        """
        url = "welllog/%s" % welllog_id
        item = self.client.get(url)
        return Welllog.from_dict(item)

    def add_welllog(self, wellbore: Wellbore, log: Welllog, *, lookup_alias: bool = False) -> None:
        """
        Add a well log to a wellbore.

        :param wellbore: Wellbore object to which the log will be added.
        :param log: Welllog object to add (modified in-place with server-assigned IDs). Curve samples are preserved locally.
        :param lookup_alias: If True, server will attempt mnemonic alias lookup on curves (e.g., auto-map curve names). Defaults to False.
        :raises ZonevuError: If wellbore not found, permission denied, or network error occurs.
        :note: The log and curve objects are updated with server-assigned IDs after creation.
        """
        url = "welllog/add/%s" % wellbore.id

        # Build a dictionary of curve samples. Null out curve samples, so they are not copied to server here.
        curveDict = dict(map(lambda c: (id(c), c.samples), log.curves))
        for curve in log.curves:
            curve.samples = None

        item = self.client.post(url, log.to_dict(), True, {'lookupalias': lookup_alias})
        server_log = log.from_dict(item)

        # Put curve samples back on source well log curves
        for curve in log.curves:
            curve.samples = curveDict[id(curve)]

        log.copy_ids_from(server_log)   # Copy server ids of logs to client.

    def delete_welllog(self, log: Welllog, delete_code: str) -> None:
        """
        Delete a well log from the server.

        :param log: Welllog object with valid ID to delete.
        :param delete_code: Confirmation code required to delete the welllog (safety mechanism).
        :raises ZonevuError: If welllog not found, permission denied, or network error occurs.
        """
        url = "welllog/delete/%s" % log.id
        self.client.delete(url, {"deletecode": delete_code})

    def get_lasfile(self, welllog: Welllog) -> Optional[str]:
        """
        Get LAS (Log ASCII Standard) file content for a well log.

        :param welllog: Welllog object with valid ID.
        :return: LAS file content as a string, or None if not available.
        :raises ZonevuError: If welllog not found or network error occurs.
        """
        url = "welllog/lasfile/%s" % welllog.id
        raw_ascii_text = self.client.get_text(url, 'ascii')
        if raw_ascii_text is None:
            return None
        # Fix up text
        # ascii_text = raw_ascii_text.replace('\\r', '')
        # ascii_text = ascii_text.replace('\\n', '\n')
        # N = len(ascii_text)
        # ascii_text = ascii_text[1:N - 1]
        ascii_text = raw_ascii_text.replace('\r', '')   # Remove carriage returns.
        return ascii_text

    def post_lasfile(self, welllog: Welllog, las_text: str) -> None:
        """
        Update the LAS (Log ASCII Standard) file content for a well log.

        :param welllog: Welllog object with valid ID to update.
        :param las_text: LAS file content as a string (ASCII-encoded).
        :raises ZonevuError: If welllog not found, permission denied, or network error occurs.
        """
        url = "welllog/lasfile/%s" % welllog.id
        txt_bytes = las_text.encode('ascii')
        self.client.post_data(url, txt_bytes)

    def create_las_file_server(self, welllog: Welllog, overwrite: bool = False):
        """
        Create or recreate a LAS file on the server from well log database data.

        :param welllog: Welllog object with valid ID.
        :param overwrite: If True, overwrite existing LAS file; if False, only create if missing. Defaults to False.
        :raises ZonevuError: If welllog not found, permission denied, or network error occurs.
        """
        url = "welllog/lasfile/instantiate/%s" % welllog.id
        self.client.post(url, {}, False, {"overwrite": overwrite})

    def load_curve_samples(self, curve: Curve):
        url = "welllog/curvedepthdatabytes/%s" % curve.id
        curve_float_bytes = self.client.get_data(url)
        tuples = np.frombuffer(curve_float_bytes, dtype=np.float32)
        curve.depths = tuples[::2]
        curve.samples = tuples[1::2]

    def load_splice_curve_samples(self, curve_group: CurveGroup):
        url = "welllog/splicecurvedepthdatabytes/%s" % curve_group.id
        curve_float_bytes = self.client.get_data(url)
        tuples = np.frombuffer(curve_float_bytes, dtype=np.float32)
        curve_group.depths = tuples[::2]
        curve_group.samples = tuples[1::2]

    def add_curve_samples(self, curve: Curve) -> None:
        url = "welllog/curvedatabytes/%s" % curve.id
        if curve.samples is not None:
            curve_float_bytes = curve.samples.tobytes()
            self.client.post_data(url, curve_float_bytes, 'application/octet-stream')

    def add_curve_group(self, welllog_id: int, curve_group: CurveGroup) -> None:
        url = "welllog/addcurvegroup/%s" % welllog_id
        item = self.client.post(url, curve_group.to_dict(), True)
        server_group = curve_group.from_dict(item)
        curve_group.copy_ids_from(server_group)   # Copy server ids of logs to client.
