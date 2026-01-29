"""
BioShield Integration Platform - Universal Import Solution
"""

import sys
import os

# الحل الشامل للمسارات
def _setup_paths():
    """Setup all possible import paths"""
    # المسار الحالي
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # جميع المسارات المحتملة
    possible_paths = [
        current_dir,                                # src/
        os.path.dirname(current_dir),               # BioShield-Integration/
        os.path.join(os.path.dirname(current_dir), 'src'),  # BioShield-Integration/src
        os.path.join(current_dir, 'adaptive'),      # src/adaptive/
        os.path.join(current_dir, 'orchestrator'),  # src/orchestrator/
    ]
    
    # إضافة المسارات الفريدة
    for path in possible_paths:
        if os.path.exists(path) and path not in sys.path:
            sys.path.insert(0, path)

# تنفيذ إعداد المسارات عند الاستيراد
_setup_paths()

# تصدير المكونات الرئيسية
try:
    from adaptive.adaptive_memory import AdaptiveMemory
    from adaptive.adaptive_engine import AdaptiveEngine
    from orchestrator.cascade_manager import CascadeManager
    HAS_COMPONENTS = True
except ImportError:
    HAS_COMPONENTS = False

__version__ = "2.0.0"
__author__ = "BioShield Team"
__all__ = ['AdaptiveMemory', 'AdaptiveEngine', 'CascadeManager'] if HAS_COMPONENTS else []
