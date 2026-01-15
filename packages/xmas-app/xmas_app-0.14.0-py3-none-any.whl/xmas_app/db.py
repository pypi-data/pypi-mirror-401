import logging

from nicegui.observables import ObservableSet
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from xplan_tools.model import model_factory
from xplan_tools.model.base import BaseFeature
from xplan_tools.model.orm import Feature, Refs

from xmas_app.settings import get_mappings, get_settings

logger = logging.getLogger("xmas_app")


def get_db_plans() -> list[dict]:
    """Get plan data from the database.

    Query the database for plan objects.

    Returns:
        list[dict]: List of dicts containing plan data, i.e. name, id, appschema, version, last update.
    """
    results = []
    try:
        with get_settings().repo.Session() as session:
            stmt = select(Feature).where(Feature.featuretype.regexp_match("^.*Plan$"))
            try:
                db_result = session.execute(stmt)
                features = db_result.unique().scalars().all()
                logger.info(f"Found {len(features)} feature(s) in DB.")
            except Exception as db_ex:
                logger.error(f"Database query failed: {db_ex}", exc_info=True)
            for feature in features:
                plan_data = {
                    "id": str(feature.id),
                    "label": feature.properties.get("name", "<Name unbekannt>"),
                    "appschema": {
                        "name": feature.appschema.upper(),
                        "version": feature.version,
                    },
                    "updated": {
                        "date": f"{feature.updated_at.strftime('%m.%d.%Y')}",
                        "time": f"{feature.updated_at.strftime('%H:%M:%S Uhr')}",
                    },
                }
                results.append(plan_data)

    except Exception as ex:
        logger.error(f"Failed to get plan data: {ex}", exc_info=True)
        raise
    return results


def get_nodes(
    id: str, features_set: ObservableSet
) -> tuple[dict, str, str, str] | None:
    """Build tree nodes for ui.tree element."""

    def build_node(feature: Feature, path: str) -> dict:
        features_set.add(feature.id)
        node = {
            "id": f"{path}.{feature.featuretype}.{feature.id}",
            "label": f"{feature.featuretype} {str(feature.id)[:8]}",
            "icon": get_icon(feature),
        }
        node["children"] = build_nodes(feature)
        return node

    def build_nodes(feature: Feature) -> list[dict]:
        model = model_factory(feature.featuretype, feature.version, feature.appschema)
        node_dict = {}
        for assoc in model.get_associations():
            prop_info = model.get_property_info(assoc)
            if prop_info["assoc_info"]["source_or_target"] == (
                "target"
                if (feature.featuretype == "FP_Plan" and assoc == "bereich")
                or (feature.featuretype == "FP_Bereich" and assoc == "gehoertZuPlan")
                else "source"
            ):
                continue
            node = {
                "id": f"{feature.featuretype}.{feature.id}.{assoc}",
                "label": assoc,
                "selectable": True,
                "icon": "link",
            }
            node_dict[assoc] = node
        for ref in feature.refs:
            path = ".".join(
                [
                    feature.featuretype,
                    str(feature.id),
                    ref.rel,
                ]
            )
            node = build_node(ref.feature_inv, path)
            node_dict[ref.rel].setdefault("children", []).append(node)

        nodes = []
        for node in node_dict.values():
            if children := node.get("children"):
                node["label"] += f" [{len(children)}]"
            nodes.append(node)
        return nodes

    def get_icon(feature: Feature):
        match feature.geometry_type:
            case "polygon":
                icon = "o_space_dashboard"
            case "line":
                icon = "show_chart"
            case "point":
                icon = "o_location_on"
            case _:
                icon = "o_text_snippet"
        return icon

    with get_settings().repo.Session() as session:
        stmt = (
            select(Feature)
            .options(
                selectinload(Feature.refs)
                .selectinload(Refs.feature_inv)
                .selectinload(Feature.refs)
                .selectinload(Refs.feature_inv)
                .selectinload(Feature.refs)
            )
            .where(Feature.id == id)
        )

        feature = session.execute(stmt).scalar_one_or_none()
        # feature = session.get(Feature, id)
        if not feature or "Plan" not in feature.featuretype:
            return

        features_set.add(feature.id)

        tree_nodes = [
            {
                "id": feature.id,
                "label": feature.properties["name"],
                "selectable": False,
                "children": build_nodes(feature),
            }
        ]

        return (
            tree_nodes,
            feature.featuretype,
            feature.id,
            feature.appschema,
        )


def _feature_to_table_row(feature: Feature) -> dict:
    extra_property = getattr(
        get_mappings().association_table.extra_properties, feature.appschema
    ).get(feature.featuretype)
    extra_property_label = feature.properties.get(extra_property, "N/A")
    return {
        "id": str(feature.id),
        "featuretype": feature.featuretype,
        "geometry_type": feature.geometry_type,
        "updated": f"{feature.updated_at.strftime('%m.%d.%Y')} {feature.updated_at.strftime('%H:%M:%S')}",
        "extra_property": f"{extra_property}={extra_property_label}"
        if extra_property
        else "N/A",
    }


def _rel_inv_is_list(feature: Feature, rel_inv: str | None) -> bool:
    # if there is no inverse relation, return True
    if not rel_inv:
        return True
    model = model_factory(feature.featuretype, feature.version, feature.appschema)
    return model.get_property_info(rel_inv)["list"]


def get_ref_objects(refs: list[str]) -> list[dict]:
    """Returns a list of data objects for existing feature references to use in table rows."""
    with get_settings().repo.Session() as session:
        stmt = select(Feature).where(Feature.id.in_(refs))
        features = session.execute(stmt).scalars().all()

    return [_feature_to_table_row(feature) for feature in features]


def get_ref_candidates(
    refs: list[str], plan_id: str, model: BaseFeature, rel: str
) -> list[dict]:
    """Returns a list of data objects for potential feature references to use in table rows."""
    prop_info = model.get_property_info(rel)
    typename = prop_info["typename"]
    featuretypes = typename if isinstance(typename, list) else [typename]
    rel_inv = model.get_property_info(rel)["assoc_info"]["reverse"]

    with get_settings().repo.Session() as session:
        plan = session.get(Feature, plan_id)
        candidates = plan.related_features(
            session, featuretypes=featuretypes, exclude_ids=refs
        )
        return [
            _feature_to_table_row(feature)
            for feature in candidates
            if _rel_inv_is_list(feature, rel_inv)
        ]
