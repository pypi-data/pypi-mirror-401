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

"""
Completions (frac) service.

List, retrieve, load, and add frac jobs and stages for a wellbore. Includes
strategies for updating stages and linking to geosteering interpretations.
"""

from ..datamodels.completions.FracEntry import FracEntry
from ..datamodels.completions.Frac import Frac
from ..datamodels.wells.Wellbore import Wellbore
from .Client import Client, ZonevuError
from typing import List
from strenum import StrEnum


class StageUpdateMethodEnum(StrEnum):
    """Strategy for updating frac stages when posting a frac."""
    Preserve = 'Preserve'           # Preserve existing stages, but append new stages
    Merge = 'Merge'                 # Merge overlapping stages
    Overwrite = 'Overwrite'         # Overwrite existing overlapping stages
    Bypass = 'Bypass'               # Do not update stages


class CompletionsService:
    """Manage frac jobs and stages, with load/add and merge strategies."""

    client: Client

    def __init__(self, c: Client):
        self.client = c

    def get_fracs(self, wellbore_id: int) -> List[FracEntry]:
        """
        Get list of frac jobs for a wellbore.
        
        :param wellbore_id: System ID of the wellbore.
        :return: List of FracEntry objects (summary data). Use :py:meth:`find_frac` to fetch full Frac objects.
        :raises ZonevuError: If wellbore not found or network error occurs.
        """
        url = "completions/fracs/%s" % wellbore_id
        items = self.client.get_list(url)
        frac_entries = [FracEntry.from_dict(w) for w in items]
        return frac_entries

    def find_frac(self, frac_id: int) -> Frac:
        """
        Get a frac job by its system ID.

        :param frac_id: Frac system ID (from FracEntry.id or catalog results).
        :return: Full Frac object with all stages and entries.
        :raises ZonevuError: If frac not found or network error occurs.
        """
        url = "completions/frac/%s" % frac_id
        item = self.client.get(url)
        frac = Frac.from_dict(item)
        return frac

    def load_fracs(self, wellbore: Wellbore) -> List[Frac]:
        """
        Load all frac jobs for a wellbore and populate the wellbore object.

        :param wellbore: Wellbore object to populate with fracs (object is modified in-place).
        :return: List of full Frac objects loaded and attached to the wellbore.
        :note: Individual frac load failures are logged but do not stop the overall loading process.
        """
        frac_entries = self.get_fracs(wellbore.id)
        wellbore.fracs = []
        for frac_entry in frac_entries:
            try:
                frac = self.find_frac(frac_entry.id)
                wellbore.fracs.append(frac)
            except ZonevuError as frac_err:
                print('Could not load frac "%s" because %s' % frac_err.message)
            except Exception as frac_err2:
                print('Could not load frac "%s" because %s' % frac_err2)
        return wellbore.fracs

    def add_frac(self, wellbore: Wellbore | int, frac: Frac) -> None:
        """
        Add a frac job (with stages) to a wellbore.

        :param wellbore: Wellbore identifier in one of the following formats:
            - Wellbore ID (int): ``add_frac(456, frac)``
            - Wellbore object: ``add_frac(wellbore, frac)``
        :param frac: Frac object with stages and entries (modified in-place with server-assigned IDs).
        :raises ZonevuError: If wellbore not found, referenced geosteering interpretations don't exist, or network error occurs.
        :note: Assumes all geosteering interpretations referenced by the frac already exist for this wellbore on the server.
        :note: The frac object is updated with server-assigned IDs after creation.
        """
        wellbore_id = wellbore if isinstance(wellbore, int) else wellbore.id
        url = "completions/frac/add/%s" % wellbore_id
        item = self.client.post(url, frac.to_dict())
        server_frac = Frac.from_dict(item)
        frac.copy_ids_from(server_frac)

    def delete_frac(self, frac: Frac, delete_code: str) -> None:
        """
        Delete a frac job from the server.

        :param frac: Frac object with valid ID to delete.
        :param delete_code: Confirmation code required to delete the frac (safety mechanism).
        :raises ZonevuError: If frac not found, permission denied, or network error occurs.
        """
        url = "completions/frac/delete/%s" % frac.id
        self.client.delete(url, {"deletecode": delete_code})

    def update_frac(self, frac: Frac, frac_update: bool, stage_update: StageUpdateMethodEnum = StageUpdateMethodEnum.Bypass) -> None:
        """
        Update a frac job and/or its stages using a specified merge strategy.

        :param frac: Frac object with updates (modified in-place with updated data).
        :param frac_update: If True, update the frac metadata itself; if False, skip frac-level updates.
        :param stage_update: Strategy for updating frac stages. Options:
            - ``StageUpdateMethodEnum.Preserve`` - Keep existing stages, append only new stages
            - ``StageUpdateMethodEnum.Merge`` - Merge overlapping stages intelligently
            - ``StageUpdateMethodEnum.Overwrite`` - Overwrite existing overlapping stages
            - ``StageUpdateMethodEnum.Bypass`` (default) - Do not update stages, only update frac metadata
        :raises ZonevuError: If frac not found, permission denied, or network error occurs.
        :note: The frac object is updated in-place with server response data.
        """
        url = "completions/frac/update/%s" % frac.id
        item = self.client.patch(url, frac.to_dict(), True, {'fracupdate': frac_update, 'stageupdate': stage_update})
        server_frac = Frac.from_dict(item)
        frac.copy_ids_from(server_frac)