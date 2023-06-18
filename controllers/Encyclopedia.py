from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.document import DocumentModel
from models.topic import TopicModel
from models.community import CommunityModel
from models.administrator_manage_community import AdministratorManageCommunityModel
from models.community_has_document_and_topic import CommunityHasDocumentAndTopicModel


class Documents(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "name", type=str, required=True, help="This field cannot be blank."
    )
    parser.add_argument(
        "description", type=str, required=False, help="This field cannot be blank."
    )
    parser.add_argument("file", required=True, help="This field cannot be blank.")
    parser.add_argument(
        "type", type=str, required=True, help="This field cannot be blank."
    )
    parser.add_argument(
        "administrator_id", type=int, required=False, help="This field cannot be blank."
    )
    parser.add_argument(
        "topic_id", type=int, required=True, help="This field cannot be blank."
    )

    @jwt_required()
    def get(self):
        return {
            "documents": [
                document.json()
                for document in DocumentModel.query.filter_by(is_active=True).all()
            ]
        }, 200

    @jwt_required()
    def post(self, community_id):
        data = Documents.parser.parse_args()
        jwt_user = get_jwt_identity()
        user_id = jwt_user["id"]

        if not TopicModel.find_by_id(data["topic_id"]):
            return {"message": "Topic not found"}, 404
        if not CommunityModel.find_by_id(community_id):
            return {"message": "Community not found"}, 404
        if not CommunityModel.is_member(user_id, community_id):
            return {"message": "User not member of community"}, 404

        if AdministratorManageCommunityModel.user_is_admin_of_community(
            user_id, community_id
        ):
            blob = data["file"].encode("utf-8")

            document = DocumentModel(
                data["name"],
                data["description"] if not data["description"] is None else "",
                blob,
                data["type"],
                user_id,
                user_id,
            )
            try:
                document.save_to_db()
            except Exception as e:
                print(e)
                return {"message": "An error occurred creating the document."}, 500

            comm_has_doc_and_topic = CommunityHasDocumentAndTopicModel(
                community_id=community_id,
                document_id=document.id,
                topic_id=data["topic_id"],
            )
            try:
                comm_has_doc_and_topic.save_to_db()
            except Exception as e:
                print(e)
                return {"message": "An error occurred creating the document."}, 500
            return {"message": "The document has been stored"}, 201

        blob = data["file"].encode("utf-8")

        document = DocumentModel(
            data["name"],
            data["description"] if not data["description"] is None else "",
            blob,
            data["type"],
            user_id
        )
        try:
            document.is_active = False
            document.save_to_db()
        except:
            return {"message": "An error occurred creating the document."}, 500

        comm_has_doc_and_topic = CommunityHasDocumentAndTopicModel(
            community_id=community_id,
            document_id=document.id,
            topic_id=data["topic_id"],
        )
        try:
            comm_has_doc_and_topic.save_to_db()
        except:
            return {"message": "An error occurred creating the relation."}, 500
        return document.json(), 201


class DocumentsByTopic(Resource):
    @jwt_required()
    def get(self, topic_id):
        if not TopicModel.find_by_id(topic_id):
            return {"message": "Topic not found"}, 404
        return {
            "documents": [
                document.json()
                for document in DocumentModel.query.filter_by(is_active=True).all()
            ]
        }, 200

class DocumentsPropouse(Resource):
    @jwt_required()
    def get(self, community_id):
        jwt_user = get_jwt_identity()
        user_id = jwt_user["id"]

        if not CommunityModel.find_by_id(community_id):
            return {"message": "Community not found"}, 404
        if not AdministratorManageCommunityModel.user_is_admin_of_community(user_id, community_id):
            return {"message": "User not admin of community"}, 404
        
        return {
            "documents": [
                document.json()
                for document in CommunityHasDocumentAndTopicModel.get_propouse_by_com(community_id)
            ]
        }, 200

class RejectDocument(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "document_id", type=int, required=True, help="This field cannot be blank."
    )

    @jwt_required()
    def post(self, community_id):
        data = RejectDocument.parser.parse_args()
        jwt_user = get_jwt_identity()
        user_id = jwt_user["id"]

        if not CommunityModel.find_by_id(community_id):
            return {"message": "Community not found"}, 404
        if not CommunityModel.find_by_id(community_id).is_member(user_id):
            return {"message": "User not member of community"}, 404
        if not AdministratorManageCommunityModel.user_is_admin_of_community(
            user_id, community_id
        ):
            return {"message": "User not admin of community"}, 404

        document = DocumentModel.find_by_id(data["document_id"])
        if not document:
            return {"message": "Document not found"}, 404

        document.delete_from_db()
        return {"message": "Document deleted"}, 200


class AcceptDocument(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "document_id", type=int, required=True, help="This field cannot be blank."
    )

    @jwt_required()
    def post(self, community_id):
        data = AcceptDocument.parser.parse_args()
        jwt_user = get_jwt_identity()
        user_id = jwt_user["id"]

        if not CommunityModel.find_by_id(community_id):
            return {"message": "Community not found"}, 404
        if not CommunityModel.find_by_id(community_id).is_member(user_id):
            return {"message": "User not member of community"}, 404
        if not AdministratorManageCommunityModel.user_is_admin_of_community(
            user_id, community_id
        ):
            return {"message": "User not admin of community"}, 404

        document = DocumentModel.find_by_id(data["document_id"])
        if not document:
            return {"message": "Document not found"}, 404

        document.is_active = True
        document.save_to_db()
        return document.json(), 200
