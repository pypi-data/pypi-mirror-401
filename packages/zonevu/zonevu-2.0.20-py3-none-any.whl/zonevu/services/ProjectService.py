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
Project listing and retrieval service.

Search projects by name, list projects per division, and fetch complete project
objects with optional related data (map layers, wells, geomodels, seismic).
Also includes utilities to locate a project by name and populate it.
"""

import time
import urllib.parse

from .CompanyService import CompanyService
from ..datamodels.Project import Project
from ..datamodels.Project import ProjectEntry
from ..datamodels.wells.Well import Well, WellEntry
from ..datamodels.Company import Division
from ..datamodels.wells.Survey import Survey
from ..datamodels.geomodels.Geomodel import Geomodel, GeomodelEntry
from ..datamodels.seismic.SeismicSurvey import SeismicSurvey, SeismicSurveyEntry
from ..services.MapService import MapService
from .Client import Client
from typing import Tuple, Union, Dict, Optional, Any, List, Set
from strenum import StrEnum


class ProjectData(StrEnum):
    """Flags for which project-related data to load (e.g., layer data)."""
    default = 'default'     # Default behavior is to not load anything extra
    layer_data = 'layer_data'
    all = 'all'             # If specified, load all data, as long as 'default' flag not present


class ProjectDataOptions:
    """Helper to interpret ProjectData flags for loading related data."""
    project_data: Set[ProjectData]

    def __init__(self, project_data: Optional[Set[ProjectData]]):
        self.project_data = project_data or set()

    def _calc_option(self, project_data: ProjectData) -> bool:
        return (project_data in self.project_data or self.all) and self.some

    @property
    def all(self):
        return ProjectData.all in self.project_data

    @property
    def some(self) -> bool:
        return ProjectData.default not in self.project_data

    @property
    def layer_data(self) -> bool:
        return self._calc_option(ProjectData.layer_data)


class ProjectService:
    """Search and fetch projects; optionally populate related domain data."""

    client: Client

    def __init__(self, c: Client):
        self.client = c

    def get_projects(self, name: Optional[str] = None, division: Optional[Union[Division, int, str]] = None) -> List[ProjectEntry]:
        """
        Get list of project catalog entries, optionally filtered by name or division.

        :param name: Optional project name fragment to match (case-insensitive, partial matching enabled).
        :param division: Optional division (business unit) filter. Accepts multiple formats:
            - Division ID (int): ``get_projects(division=42)``
            - Division name (str): ``get_projects(division='north_division')``
            - Division object: ``get_projects(division=division_obj)``
            - None (default): Search all divisions user is authorized for
        :return: List of ProjectEntry objects (summary data only, not full project objects).
        :note: If no search parameters provided, returns all projects accessible to the account.
        :note: Use :py:meth:`get` to retrieve full Project objects with optional child data (wells, maps, etc.).
        """
        return self.find_by_name(match_token = name, exact_match=False, division = division)

    def get(self, identifier: Optional[Union[ProjectEntry, int, str]], project_data: Optional[Set[ProjectData]] = None) -> Optional[Project]:
        """
        Get a full project object based on a project identifier with optional child data.

        :param identifier: Project identifier in one of the following formats:
            - Project ID (int): ``get(1227)`` - System ID from :py:meth:`get_projects`
            - Project name (str): ``get('Exploration North')`` - Project name (uses :py:meth:`get_first_named`)
            - ProjectEntry object: ``get(project_entry)`` - From catalog search results
        :param project_data: Optional set of child data to load. Accepts any combination of:
            - ``{ProjectData.layer_data}`` - Load map layers
            - ``{ProjectData.all}`` - Load all available child data
            - ``None`` (default) - Load only basic project metadata (including wells list)
        :return: Full Project object if found, None if not found.
        :note: Project objects include a list of wells in the project via the ``wells`` property.
        :raises ZonevuError: If the project identifier is invalid or network error occurs.
        """
        project: Optional[Project] = None
        if isinstance(identifier, ProjectEntry):
            project = self.find_project(identifier.id)
        elif isinstance(identifier, int):
            project =  self.find_project(identifier)
        elif isinstance(identifier, str):
            project =  self.get_first_named(identifier)
        else:
            return None

        if project is None:
            return None

        if project_data is not None:
            self.load_project(project, project_data)
        return project

    def find_by_name(self, match_token: Optional[str] = None, exact_match: Optional[bool] = True, division: Optional[Union[Division, int, str]] = None,
                     page: Optional[int] = 0) -> List[ProjectEntry]:
        """
        Find projects by name fragment or exact name match across all divisions or a specific division.

        :param match_token: Name or name fragment to search for (case-insensitive). If None, returns all projects in specified division(s).
        :param exact_match: If True, perform exact name match; if False, allow partial/prefix matching.
        :param division: Optional division filter. Accepts multiple formats:
            - Division ID (int): ``find_by_name('Exploration North', division=42)``
            - Division name (str): ``find_by_name('Exploration North', division='north')``
            - Division object: ``find_by_name('Exploration North', division=division_obj)``
            - None (default): Search all divisions user is authorized for
        :param page: Internal pagination parameter (usually ignore; method handles pagination automatically).
        :return: List of ProjectEntry objects (summary data). Use :py:meth:`get` to fetch full Project objects.
        :note: Automatically handles pagination; retrieves all matching results across multiple API calls.
        :raises ZonevuError: If division name is invalid or network error occurs.
        """
        url = "projects"
        max_pages = 50     # This means that it won't do more than 50 round trips to retrieve search result pages.
        params = {"exactmatch": str(exact_match)}
        all_entries: list[ProjectEntry] = []
        more = True
        if match_token is not None:
            params["name"] = urllib.parse.quote_plus(match_token)


        if division is not None:
            division_id = -1
            if isinstance(division, str):
                divisions = CompanyService(self.client).get_divisions()
                division_obj = next((d for d in divisions if d.name.lower() == division.lower()), None)
                if division_obj is None:
                    raise Exception(f'no such division "{division}"')
                division_id = division_obj.id
            elif isinstance(division, Division):
                division_id = division.id
            elif isinstance(division, int):
                division_id = division
            else:
                raise Exception(f'illegal division type encountered')
            params["divisionid"] = division_id

        counter = 0
        while more:
            params["page"] = str(page)
            wells_response = self.client.get_dict(url, params, False)
            items = wells_response['Projects']
            more = wells_response['More']
            page = wells_response['Page']
            entries = [ProjectEntry.from_dict(w) for w in items]
            all_entries.extend(entries)
            counter += 1
            if counter > max_pages:
                break               # Safety check. Limits us to 500 iterations, which is 250,000 wells.
            time.sleep(0.050)       # Pause for 50 ms so as not to run into trouble with webapi throttling.

        return all_entries

    def get_first_named(self, name: str) -> Optional[Project]:
        """
        Find the first project with the specified name and return the full project object.

        :param name: Project name to search for (exact match on full name).
        :return: Full Project object if found, None if not found.
        :note: Returns only the first match if multiple projects have similar names.
        :raises ZonevuError: If network error occurs.
        """
        project_entries = self.find_by_name(name)
        if len(project_entries) == 0:
            return None
        entry = project_entries[0]
        project = self.find_project(entry.id)
        return project

    def project_exists(self, name: str) -> Tuple[bool, int]:
        """
        Check if a project exists by name and return the project ID if found.

        :param name: Project name to search for (exact match).
        :return: Tuple of (exists: bool, project_id: int)
                 - exists: True if project found, False otherwise
                 - project_id: System ID if exists, -1 if not found
        """
        projects = self.find_by_name(name)
        exists = len(projects) > 0
        project_id = projects[0].id if exists else -1
        return exists, project_id

    def exists(self, identifier: Union[str, int]) -> bool:
        """
        Check if a project exists by ID or name.

        :param identifier: Project identifier in one of the following formats:
            - Project ID (int): ``exists(1227)`` - System ID to check
            - Project name (str): ``exists('Exploration North')`` - Name fragment to search for
        :return: True if a project with the given identifier exists, False otherwise.
        :note: For string identifiers, uses partial name matching (same as :py:meth:`find_by_name` with exact_match=False).
        """
        if isinstance(identifier, int):
            project = self.find_project(identifier)
            return project is not None
        elif isinstance(identifier, str):
            projects = self.find_by_name(identifier)
            exists = len(projects) > 0
            return exists

    def find_project(self, project_id: int) -> Optional[Project]:
        """
        Get a project by its system ID.

        :param project_id: Project system ID (from ProjectEntry.id or catalog results).
        :return: Full Project object if found, None if not found.
        :raises ZonevuError: If network error occurs.
        """
        url = "project/%s" % project_id
        item = self.client.get(url)
        if item is None:
            return None
        project = Project.from_dict(item)
        return project

    def load_project(self, project: Project, project_data: Optional[Set[ProjectData]]) -> None:
        """
        Load optional child data into an existing project object.

        :param project: The project object to populate with additional data.
        :param project_data: Set of child data to load. Accepts any combination of:
            - ``{ProjectData.layer_data}`` - Load map layers
            - ``{ProjectData.all}`` - Load all available child data
        :note: This method modifies the project object in-place by fetching fresh data from the server.
        """
        options = ProjectDataOptions(project_data)
        loaded_project = self.find_project(project.id)
        project.merge_from(loaded_project)

        if options.layer_data:
            try:
                map_svc = MapService(self.client)
                for layer in project.layers:
                    map_svc.load_user_layer(layer)
            except Exception as err:
                print('Could not load project layers because %s' % err)

    def create_project(self, project: Project) -> None:
        """
        Create a new project on the server.

        :param project: Project object to create (will be modified with server-assigned ID).
        :raises ZonevuError: If project creation fails or network error occurs.
        :note: The project object is updated in-place with the server-assigned ID after creation.
        """
        url = "project/create"
        item = self.client.post(url, project.to_dict())
        server_project = Survey.from_dict(item)
        project.copy_ids_from(server_project)

    def delete_project(self, identifier: Union[int, ProjectEntry, Project], delete_code: str) -> None:
        """
        Delete a project from the server.

        :param identifier: Project identifier in one of the following formats:
            - Project ID (int): ``delete_project(1227, 'DELETE_CODE')``
            - ProjectEntry object: ``delete_project(project_entry, 'DELETE_CODE')``
            - Project object: ``delete_project(project, 'DELETE_CODE')``
        :param delete_code: Confirmation code required to delete the project (safety mechanism).
        :raises ZonevuError: If project not found or deletion fails.
        """
        project_id: int = identifier.id if isinstance(identifier, ProjectEntry) or isinstance(identifier, Project) else int(identifier)
        url = "project/delete/%s" % project_id
        url_params: Dict[str, Any] = {"deletecode": delete_code}
        self.client.delete(url, url_params)

    def add_well(self, project: Union[Project, ProjectEntry, int], well: Union[Well, WellEntry, int]) -> None:
        """
        Add a single well to a project.

        :param project: Project identifier in one of the following formats:
            - Project ID (int): ``add_well(1227, well)``
            - ProjectEntry object: ``add_well(project_entry, well)``
            - Project object: ``add_well(project, well)``
        :param well: Well identifier in one of the following formats:
            - Well ID (int): ``add_well(project, 456)``
            - WellEntry object: ``add_well(project, well_entry)``
            - Well object: ``add_well(project, well)``
        :raises ZonevuError: If well already in project, permission denied, or network error occurs.
        :note: See :py:meth:`add_wells` to add multiple wells at once.
        """
        project_id = project if isinstance(project, int) else project.id
        well_id = well if isinstance(well, int) else well.id
        url = "project/%s/addwell/%s" % (project_id, well_id)
        self.client.post(url, {}, False)

    def add_wells(self, project: Union[Project, ProjectEntry, int], wells: List[Union[Well, WellEntry, int]], update_boundary: bool = True) -> None:
        """
        Add multiple wells to a project.

        :param project: Project identifier in one of the following formats:
            - Project ID (int): ``add_wells(1227, wells_list)``
            - ProjectEntry object: ``add_wells(project_entry, wells_list)``
            - Project object: ``add_wells(project, wells_list)``
        :param wells: List of well identifiers. Each can be:
            - Well ID (int): ``add_wells(project, [456, 789])``
            - WellEntry objects: ``add_wells(project, [well_entry1, well_entry2])``
            - Well objects: ``add_wells(project, [well1, well2])``
            - Mixed types supported: ``add_wells(project, [456, well_entry, well_obj])``
        :param update_boundary: If True (default), expand project boundary to include new wells.
                               If False, keep existing boundary unchanged.
        :raises ZonevuError: If wells already in project, permission denied, or network error occurs.
        :note: More efficient than calling :py:meth:`add_well` multiple times.
        """
        project_id = project if isinstance(project, int) else project.id
        well_ids: List[int] = [well if isinstance(well, int) else well.id for well in wells]
        url = f'project/addwells/{project_id}'
        self.client.post(url, well_ids, False, {"updateboundary": update_boundary})

    def remove_well(self, project: Union[Project, ProjectEntry], well: Union[Well, WellEntry]) -> None:
        """
        Remove a well from a project.

        :param project: Project identifier (ProjectEntry or Project object with valid ID).
        :param well: Well identifier (WellEntry or Well object with valid ID).
        :raises ZonevuError: If well not in project, permission denied, or network error occurs.
        """
        url = "project/%s/removewell/%s" % (project.id, well.id)
        self.client.post(url, {}, False)

    def add_geomodel(self, project: Union[Project, ProjectEntry], geomodel: Union[Geomodel, GeomodelEntry]) -> None:
        """
        Associate a geomodel with a project.

        :param project: Project identifier (ProjectEntry or Project object with valid ID).
        :param geomodel: Geomodel identifier (GeomodelEntry or Geomodel object with valid ID).
        :raises ZonevuError: If geomodel already linked, permission denied, or network error occurs.
        """
        url = "project/%s/linkgeomodel/%s" % (project.id, geomodel.id)
        self.client.post(url, {}, False)

    def remove_geomodel(self, project: Union[Project, ProjectEntry], geomodel: Union[Geomodel, GeomodelEntry]) -> None:
        """
        Remove the association of a geomodel from a project.

        :param project: Project identifier (ProjectEntry or Project object with valid ID).
        :param geomodel: Geomodel identifier (GeomodelEntry or Geomodel object with valid ID).
        :raises ZonevuError: If geomodel not linked, permission denied, or network error occurs.
        """
        url = "project/%s/unlinkgeomodel/%s" % (project.id, geomodel.id)
        self.client.post(url, {}, False)

    def add_seismicsurvey(self, project: Union[Project, ProjectEntry], survey: Union[SeismicSurvey, SeismicSurveyEntry]) -> None:
        """
        Associate a seismic survey with a project

        :param project:
        :param survey:
        :return:
        """
        url = "project/%s/linkseismic/%s" % (project.id, survey.id)
        self.client.post(url, {}, False)

    def remove_seismicsurvey(self, project: Union[Project, ProjectEntry], survey: Union[SeismicSurvey, SeismicSurveyEntry]) -> None:
        """
        Remove the association of a seismic survey with a project

        :param project:
        :param survey:
        :return:
        """
        url = "project/%s/unlinkseismic/%s" % (project.id, survey.id)
        self.client.post(url, {}, False)

    # TODO: add method for setting the strat column on the project.