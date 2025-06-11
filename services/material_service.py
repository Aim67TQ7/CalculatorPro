from typing import List, Dict, Any
from data.materials import MATERIAL_DATABASE

class MaterialService:
    def __init__(self):
        self.materials = MATERIAL_DATABASE

    def get_all_materials(self) -> List[Dict[str, Any]]:
        """Get all materials from the database"""
        return self.materials

    def get_material_by_name(self, name: str) -> Dict[str, Any]:
        """Get specific material by name"""
        for material in self.materials:
            if material['name'].lower() == name.lower():
                return material
        return None

    def get_materials_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get materials by category (e.g., 'Agricultural', 'Chemical', etc.)"""
        return [mat for mat in self.materials if mat.get('category', '').lower() == category.lower()]

    def get_bulk_density(self, material_name: str, unit_system: str = 'imperial') -> float:
        """Get bulk density for a material in specified unit system"""
        material = self.get_material_by_name(material_name)
        if not material:
            return None
        
        if unit_system.lower() == 'metric':
            return material['bulk_density_metric']
        else:
            return material['bulk_density_imperial']

    def search_materials(self, query: str) -> List[Dict[str, Any]]:
        """Search materials by name or description"""
        query_lower = query.lower()
        return [mat for mat in self.materials 
                if query_lower in mat['name'].lower() or 
                query_lower in mat.get('description', '').lower()]

    def get_material_properties(self, material_name: str) -> Dict[str, Any]:
        """Get all properties for a specific material"""
        material = self.get_material_by_name(material_name)
        if material:
            return {
                'name': material['name'],
                'bulk_density_metric': material['bulk_density_metric'],
                'bulk_density_imperial': material['bulk_density_imperial'],
                'angle_of_repose': material['angle_of_repose'],
                'particle_size': material['particle_size'],
                'abrasiveness': material['abrasiveness'],
                'flowability': material['flowability'],
                'category': material.get('category', 'General')
            }
        return None
