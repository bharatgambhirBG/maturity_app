import os
from sqlalchemy.orm import Session
from data.repository import Repository


class AssessmentService:

    @staticmethod
    def initialize_assessment(
        session: Session,
        product_name: str,
        version: str,
        assessed_by: str,
        question_model: dict,
    ):
        assessment = Repository.create_assessment(
            session=session,
            product_name=product_name,
            version=version,
            assessed_by=assessed_by,
        )

        question_map: dict[str, int] = {}

        for d in question_model["domains"]:
            domain = Repository.create_domain(
                session=session,
                assessment_id=assessment.id,
                domain_id=d["id"],
                name=d["name"],
            )

            for sd in d["subdomains"]:
                subdomain = Repository.create_subdomain(
                    session=session,
                    domain_id=domain.id,
                    subdomain_id=sd["id"],
                    name=sd["name"],
                )

                for q in sd["questions"]:
                    db_q = Repository.create_question(
                        session=session,
                        subdomain_id=subdomain.id,
                        question_id=q["id"],
                        text=q["text"],
                        help_text=q.get("help", ""),
                    )
                    question_map[q["id"]] = db_q.id

        return assessment, question_map

    @staticmethod
    def save_responses(session: Session, assessment_id: int, responses: dict):
        upload_dir = f"uploads/assessment_{assessment_id}"
        os.makedirs(upload_dir, exist_ok=True)

        for qid, data in responses.items():
            q_db_id = data.get("question_db_id")
            if q_db_id is None:
                continue

            evidence_paths = []
            files = data.get("files") or []
            for f in files:
                file_path = os.path.join(upload_dir, f.name)
                with open(file_path, "wb") as out:
                    out.write(f.getbuffer())
                evidence_paths.append(file_path)

            Repository.save_response(
                session=session,
                assessment_id=assessment_id,
                question_id=q_db_id,
                data=data,
                evidence_paths=evidence_paths,
            )