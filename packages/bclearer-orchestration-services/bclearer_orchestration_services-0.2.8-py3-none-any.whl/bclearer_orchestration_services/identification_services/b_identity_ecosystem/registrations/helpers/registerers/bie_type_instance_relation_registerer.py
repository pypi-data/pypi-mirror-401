# from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.bie_core_relation_types import BieCoreRelationTypes
# from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_ids import BieIds
# from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_id_registers import BieIdRegisters
# from bclearer_orchestration_services.identification_services.b_identity_ecosystem.registrations.helpers.registerers.bie_relation_registerer import register_bie_relation
#
#
# # TODO: this is only type instances - need to redesign!!!!!
# def register_bie_type_instance_relation(
#         bie_place_1_id: BieIds,
#         bie_place_2_id: BieIds,
#         bie_id_relations_register: BieIdRegisters) \
#         -> None:
#
#     bie_relation_type_id = \
#         BieCoreRelationTypes.BIE_TYPES_INSTANCES.item_bie_identity
#
#     register_bie_relation(
#         bie_place_1_id=bie_place_1_id,
#         bie_place_2_id=bie_place_2_id,
#         bie_relation_type_id=bie_relation_type_id,
#         bie_id_relations_register=bie_id_relations_register)
# #     if bie_place_1_id is None:
# #         raise \
# #             Exception(
# #                 'Parameter bie_item_id is None or empty.')
# #
# #     bie_type_instance_already_registered = \
# #         __check_and_report_if_bie_type_instance_already_registered(
# #             bie_type_id=bie_place_2_id,
# #             bie_instance_id=bie_place_1_id,
# #             bie_id_types_instances_register=bie_id_relations_register)
# #
# #     if bie_type_instance_already_registered:
# #         return
# #
# #     bie_relation_type_id = \
# #         BieRelationTypes.BIE_TYPES_INSTANCES.item_bie_identity
# #
# #     new_row = \
# #         [bie_place_1_id, bie_place_2_id, bie_relation_type_id]
# #
# #     bie_id_relations_register_columns = \
# #         BIE_REGISTRY_REGISTERS_COLUMNS_DICTIONARY[
# #             BieRegistriesRegistersTypes.BIE_ID_RELATIONS_REGISTERS]
# #
# #     bie_id_relations_dataframe_row = \
# #         pandas.Series(
# #             new_row,
# #             index=bie_id_relations_register_columns).to_frame().T
# #
# #     bie_id_relations_register.concatenate_dataframe(
# #         dataframe=bie_id_relations_dataframe_row)
# #
# #
# # def __check_and_report_if_bie_type_instance_already_registered(
# #         bie_type_id: BieIds,
# #         bie_instance_id: BieIds,
# #         bie_id_types_instances_register: BieRegisters) \
# #         -> bool:
# #     dataframe = \
# #         bie_id_types_instances_register.get_bie_register_dataframe()
# #
# #     instance_column_name = \
# #         BieColumnNames.BIE_PLACE_1_IDS.b_enum_item_name
# #
# #     type_column_name = \
# #         BieColumnNames.BIE_PLACE_2_IDS.b_enum_item_name
# #
# #     bie_type_instance_already_registered = (
# #         (dataframe[instance_column_name] == bie_instance_id) &
# #         (dataframe[type_column_name] == bie_type_id)).any()
# #
# #     if bie_type_instance_already_registered:
# #         message = \
# #             'WARNING: Bie relation id already registered: ' \
# #             + str(bie_instance_id) \
# #             + ' --> ' \
# #             + str(bie_type_id)
# #
# #         log_message(
# #             message=message)
# #
# #         return \
# #             True
# #
# #     return \
# #         False
