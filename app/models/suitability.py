"""Model for user suitability profiles and risk assessment"""
from datetime import datetime
from app.config.extensions import db
from sqlalchemy.sql import func

class SuitabilityProfile(db.Model):
    __tablename__ = "suitability_profiles"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    family_id = db.Column(db.Integer, db.ForeignKey("family.id"), nullable=False)
    
    # Risk Profile
    risk_tolerance = db.Column(db.String(20), nullable=False)  # conservative, moderate, aggressive
    investment_horizon = db.Column(db.String(20), nullable=False)  # short_term, medium_term, long_term
    liquidity_needs = db.Column(db.String(20), nullable=False)  # low, medium, high
    
    # Financial Situation
    annual_income = db.Column(db.Float, nullable=True)
    net_worth = db.Column(db.Float, nullable=True)
    investment_experience = db.Column(db.String(20), nullable=False)  # beginner, intermediate, advanced
    
    # Investment Goals
    primary_goal = db.Column(db.String(50), nullable=False)  # capital_preservation, income, growth, speculation
    secondary_goals = db.Column(db.JSON, nullable=True)  # List of secondary goals
    
    # Risk Assessment Scores (0-100)
    market_risk_score = db.Column(db.Integer, default=0)
    credit_risk_score = db.Column(db.Integer, default=0)
    liquidity_risk_score = db.Column(db.Integer, default=0)
    currency_risk_score = db.Column(db.Integer, default=0)
    overall_risk_score = db.Column(db.Integer, default=0)
    
    # Constraints
    investment_constraints = db.Column(db.JSON, nullable=True)  # Religious, ethical, legal constraints
    preferred_asset_classes = db.Column(db.JSON, nullable=True)  # Preferred asset classes
    excluded_asset_classes = db.Column(db.JSON, nullable=True)  # Excluded asset classes
    
    # Metadata
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    # Relationships
    user = db.relationship("User", back_populates="suitability_profiles")
    family = db.relationship("Family", back_populates="suitability_profiles")
    
    def __repr__(self):
        return f"<SuitabilityProfile(user_id={self.user_id}, family_id={self.family_id}, risk_tolerance={self.risk_tolerance})>"
    
    @property
    def risk_level_description(self):
        """Get human-readable risk level description"""
        if self.overall_risk_score <= 30:
            return "Baixo Risco"
        elif self.overall_risk_score <= 60:
            return "Médio Risco"
        else:
            return "Alto Risco"
    
    @property
    def recommended_asset_allocation(self):
        """Get recommended asset allocation based on profile"""
        if self.risk_tolerance == "conservative":
            return {
                "renda_fixa": 70,
                "renda_variavel": 20,
                "fundo_imobiliario": 10
            }
        elif self.risk_tolerance == "moderate":
            return {
                "renda_fixa": 50,
                "renda_variavel": 40,
                "fundo_imobiliario": 10
            }
        else:  # aggressive
            return {
                "renda_fixa": 30,
                "renda_variavel": 60,
                "fundo_imobiliario": 10
            }
    
    def calculate_risk_score(self):
        """Calculate overall risk score based on profile"""
        try:
            # Base score from risk tolerance
            base_scores = {
                "conservative": 20,
                "moderate": 50,
                "aggressive": 80
            }
            
            base_score = base_scores.get(self.risk_tolerance, 50)
            
            # Adjustments based on other factors
            adjustments = 0
            
            # Investment horizon adjustment
            horizon_adjustments = {
                "short_term": -10,
                "medium_term": 0,
                "long_term": 10
            }
            adjustments += horizon_adjustments.get(self.investment_horizon, 0)
            
            # Liquidity needs adjustment
            liquidity_adjustments = {
                "low": 10,
                "medium": 0,
                "high": -10
            }
            adjustments += liquidity_adjustments.get(self.liquidity_needs, 0)
            
            # Investment experience adjustment
            experience_adjustments = {
                "beginner": -10,
                "intermediate": 0,
                "advanced": 10
            }
            adjustments += experience_adjustments.get(self.investment_experience, 0)
            
            # Calculate final score
            final_score = base_score + adjustments
            
            # Ensure score is within 0-100 range
            self.overall_risk_score = max(0, min(100, final_score))
            
            return self.overall_risk_score
            
        except Exception as e:
            # Log error and return default score
            return 50
    
    def get_compatibility_score(self, portfolio_allocation: dict) -> float:
        """Calculate compatibility score between profile and current portfolio"""
        try:
            if not portfolio_allocation:
                return 0.0
            
            recommended = self.recommended_asset_allocation
            current = portfolio_allocation
            
            # Calculate weighted compatibility score
            total_compatibility = 0
            total_weight = 0
            
            for asset_class in recommended:
                if asset_class in current:
                    recommended_pct = recommended[asset_class]
                    current_pct = current.get(asset_class, 0)
                    
                    # Calculate compatibility for this asset class
                    compatibility = 100 - abs(recommended_pct - current_pct)
                    compatibility = max(0, compatibility)  # Ensure non-negative
                    
                    total_compatibility += compatibility * recommended_pct
                    total_weight += recommended_pct
            
            if total_weight == 0:
                return 0.0
            
            return round(total_compatibility / total_weight, 2)
            
        except Exception as e:
            return 0.0
    
    def get_recommendations(self, portfolio_allocation: dict) -> list:
        """Get investment recommendations based on profile and portfolio"""
        try:
            recommendations = []
            compatibility_score = self.get_compatibility_score(portfolio_allocation)
            
            if compatibility_score < 70:
                recommendations.append("Considerar rebalanceamento da carteira para melhor alinhamento com o perfil de risco")
            
            recommended = self.recommended_asset_allocation
            current = portfolio_allocation
            
            # Specific recommendations for each asset class
            for asset_class, target_pct in recommended.items():
                current_pct = current.get(asset_class, 0)
                diff = target_pct - current_pct
                
                if abs(diff) > 10:  # More than 10% difference
                    if diff > 0:
                        recommendations.append(f"Aumentar alocação em {asset_class.replace('_', ' ').title()} em {abs(diff):.1f}%")
                    else:
                        recommendations.append(f"Reduzir alocação em {asset_class.replace('_', ' ').title()} em {abs(diff):.1f}%")
            
            # Risk-specific recommendations
            if self.overall_risk_score > 70 and self.risk_tolerance == "conservative":
                recommendations.append("Perfil de risco muito alto para tolerância conservadora - considerar redução de exposição")
            
            if self.overall_risk_score < 30 and self.risk_tolerance == "aggressive":
                recommendations.append("Perfil de risco muito baixo para tolerância agressiva - considerar aumento de exposição")
            
            return recommendations
            
        except Exception as e:
            return ["Erro ao gerar recomendações"]
    
    def to_dict(self):
        """Convert profile to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'family_id': self.family_id,
            'risk_tolerance': self.risk_tolerance,
            'investment_horizon': self.investment_horizon,
            'liquidity_needs': self.liquidity_needs,
            'annual_income': self.annual_income,
            'net_worth': self.net_worth,
            'investment_experience': self.investment_experience,
            'primary_goal': self.primary_goal,
            'secondary_goals': self.secondary_goals,
            'market_risk_score': self.market_risk_score,
            'credit_risk_score': self.credit_risk_score,
            'liquidity_risk_score': self.liquidity_risk_score,
            'currency_risk_score': self.currency_risk_score,
            'overall_risk_score': self.overall_risk_score,
            'investment_constraints': self.investment_constraints,
            'preferred_asset_classes': self.preferred_asset_classes,
            'excluded_asset_classes': self.excluded_asset_classes,
            'risk_level_description': self.risk_level_description,
            'recommended_asset_allocation': self.recommended_asset_allocation,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_active': self.is_active
        }
