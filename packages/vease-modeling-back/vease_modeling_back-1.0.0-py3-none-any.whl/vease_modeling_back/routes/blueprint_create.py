# Standard library imports
import os

# Third party imports
import flask
import flask_cors  # type: ignore[import-untyped]
import opengeode
from opengeodeweb_microservice.schemas import get_schemas_dict
from opengeodeweb_back import geode_functions, utils_functions
from opengeodeweb_back.geode_objects.geode_edged_curve3d import GeodeEdgedCurve3D

# Local application imports
from . import schemas

schemas_dict = get_schemas_dict(os.path.join(os.path.dirname(__file__), "schemas"))

routes = flask.Blueprint("create_routes", __name__)
flask_cors.CORS(routes)


@routes.route(schemas_dict["aoi"]["route"], methods=schemas_dict["aoi"]["methods"])
def create_aoi() -> flask.Response:
    """Endpoint to create an Area of Interest (AOI) as an EdgedCurve3D."""
    utils_functions.validate_request(flask.request, schemas_dict["aoi"])
    params = schemas.Aoi.from_dict(flask.request.get_json())

    # Create the edged curve
    edged_curve = GeodeEdgedCurve3D()
    builder = edged_curve.builder()
    builder.set_name(params.name)

    # Create vertices first
    for point in params.points:
        builder.create_point(opengeode.Point3D([point.x, point.y, params.z]))

    # Create edges between consecutive vertices and close the loop
    num_vertices = len(params.points)
    for i in range(num_vertices):
        next_i = (i + 1) % num_vertices
        builder.create_edge_with_vertices(i, next_i)

    # Save and get info
    result = utils_functions.generate_native_viewable_and_light_viewable_from_object(
        edged_curve
    )
    return flask.make_response(result, 200)


@routes.route(schemas_dict["voi"]["route"], methods=schemas_dict["voi"]["methods"])
def create_voi() -> flask.Response:
    """Endpoint to create a Volume of Interest (VOI) as an EdgedCurve3D (a bounding box/prism)."""
    utils_functions.validate_request(flask.request, schemas_dict["voi"])
    params = schemas.Voi.from_dict(flask.request.get_json())

    aoi_data = geode_functions.get_data_info(params.aoi_id)
    if not aoi_data:
        flask.abort(404, f"AOI with id {params.aoi_id} not found")

    aoi_object = geode_functions.load_geode_object(params.aoi_id)
    if not isinstance(aoi_object, GeodeEdgedCurve3D):
        flask.abort(400, f"AOI with id {params.aoi_id} is not a GeodeEdgedCurve3D")

    aoi_curve = aoi_object.edged_curve
    nb_points = aoi_curve.nb_vertices()

    edged_curve = GeodeEdgedCurve3D()
    builder = edged_curve.builder()
    builder.set_name(params.name)

    for point_id in range(nb_points):
        aoi_point = aoi_curve.point(point_id)
        builder.create_point(
            opengeode.Point3D([aoi_point.value(0), aoi_point.value(1), params.z_min])
        )

    for point_id in range(nb_points):
        aoi_point = aoi_curve.point(point_id)
        builder.create_point(
            opengeode.Point3D([aoi_point.value(0), aoi_point.value(1), params.z_max])
        )

    for point_id in range(nb_points):
        next_point = (point_id + 1) % nb_points
        builder.create_edge_with_vertices(point_id, next_point)
        builder.create_edge_with_vertices(point_id + nb_points, next_point + nb_points)
        builder.create_edge_with_vertices(point_id, point_id + nb_points)

    result = utils_functions.generate_native_viewable_and_light_viewable_from_object(
        edged_curve
    )
    return flask.make_response(result, 200)
