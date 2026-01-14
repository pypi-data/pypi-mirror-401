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
Wellbore survey service.

List, retrieve, and load wellbore trajectory surveys and their stations for a
given wellbore. Supports adding new surveys to a wellbore.
"""

from ..datamodels.wells.Survey import Survey
from ..datamodels.wells.Station import Station
from ..datamodels.wells.Wellbore import Wellbore
from .Client import Client
from typing import List


class SurveyService:
    """List, find, and load deviation surveys and stations for a wellbore."""

    client: Client

    def __init__(self, c: Client):
        self.client = c

    def get_surveys(self, wellbore_id: int) -> list[Survey]:
        """
        Get list of wellbore surveys for a wellbore.

        :param wellbore_id: System ID of the wellbore.
        :return: List of Survey objects (basic data). Use :py:meth:`find_survey` to fetch full survey with all stations.
        :raises ZonevuError: If wellbore not found or network error occurs.
        """
        url = "surveys/%s" % wellbore_id
        items = self.client.get_list(url)
        surveys = [Survey.from_dict(w) for w in items]
        return surveys

    def find_survey(self, survey_id: int) -> Survey:
        """
        Get a full survey with all station data by its system ID.

        :param survey_id: Survey system ID (from Survey.id or catalog results).
        :return: Full Survey object with all stations populated.
        :raises ZonevuError: If survey not found or network error occurs.
        """
        url = "survey/%s" % survey_id
        item = self.client.get(url)
        survey = Survey.from_dict(item)
        return survey

    def load_survey(self, survey: Survey) -> Survey:
        """
        Load full survey data into an existing survey object.

        :param survey: Survey object to populate with full data (object is modified in-place).
        :return: The same survey object, now populated with complete data.
        """
        full_survey = self.find_survey(survey.id)
        for field, value in vars(full_survey).items():
            setattr(survey, field, value)
        return survey

    def load_surveys(self, wellbore: Wellbore) -> list[Survey]:
        """
        Load all wellbore surveys with full station data for a wellbore.

        :param wellbore: Wellbore object to populate with complete surveys (modified in-place).
        :return: List of full Survey objects with all stations attached to the wellbore.
        """
        surveys = self.get_surveys(wellbore.id)
        wellbore.surveys = []
        for survey in surveys:
            complete_survey = self.find_survey(survey.id)
            wellbore.surveys.append(complete_survey)
        return surveys

    def add_survey(self, wellbore: Wellbore, survey: Survey) -> None:
        """
        Add a survey to a wellbore.

        :param wellbore: Wellbore object to which the survey will be added.
        :param survey: Survey object to add (modified in-place with server-assigned IDs).
        :raises ZonevuError: If wellbore not found, permission denied, or network error occurs.
        :note: The survey object is updated with server-assigned IDs after creation.
        """
        url = "survey/add/%s" % wellbore.id
        item = self.client.post(url, survey.to_dict())
        server_survey = Survey.from_dict(item)
        survey.copy_ids_from(server_survey)

    def delete_survey(self, survey: Survey, delete_code: str) -> None:
        """
        Delete a survey from the server.

        :param survey: Survey object with valid ID to delete.
        :param delete_code: Confirmation code required to delete the survey (safety mechanism).
        :raises ZonevuError: If survey not found, permission denied, or network error occurs.
        """
        url = "survey/delete/%s" % survey.id
        self.client.delete(url, {"deletecode": delete_code})

    def add_stations(self, survey: Survey, stations: List[Station]) -> List[Station]:
        """
        Add survey stations to an existing survey.

        :param survey: Survey object to add stations to (must have valid ID).
        :param stations: List of Station objects to add.
        :return: List of Station objects as returned from the server with assigned IDs.
        :raises ZonevuError: If survey not found, permission denied, or network error occurs.
        """
        url = "survey/add-stations/%s" % survey.id
        data = [s.to_dict() for s in stations]
        items = self.client.post(url, data)
        if isinstance(items, List):
            surveys_server = [Station.from_dict(w) for w in items]
            return surveys_server
        return []

    def update_survey(self, survey: Survey) -> None:
        """
        Update a survey on the server.

        :param survey: Survey object with updates (modified in-place with updated server data).
        :raises ZonevuError: If survey not found, permission denied, or network error occurs.
        :note: The survey object is updated with any changes from the server response.
        """
        url = "survey/update"
        item = self.client.post(url, survey.to_dict())
        server_survey = Survey.from_dict(item)
        survey.copy_ids_from(server_survey)



