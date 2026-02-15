class ReportService:

    @staticmethod
    def spider_chart_data(domains):
        return {
            "labels": [d.name for d in domains],
            "values": [d.weighted_maturity for d in domains]
        }

    @staticmethod
    def risk_heatmap_data(domains):
        return [
            {"domain": d.name, "risk": d.risk_score}
            for d in domains
        ]

    @staticmethod
    def technical_debt_data(domains):
        return [
            {"domain": d.name, "tdi": d.tdi}
            for d in domains
        ]

    @staticmethod
    def modernization_curve(metrics):
        return metrics.MCE

    @staticmethod
    def executive_summary(metrics):
        return {
            "architecture_sustainability": metrics.ASS,
            "technical_debt_index": metrics.TDI,
            "scalability_ceiling": metrics.SCS,
            "security_risk": metrics.SCRS,
            "operational_resilience": metrics.ORS,
            "synergy_potential": metrics.SPS,
            "modernization_cost": metrics.MCE
        }