"""中国历史离线数据仓库 V1。

历史沿革：V1 版本提供了 Source→Raw→Staging→Normalize→Link→Validate→Export 管线
与旧 Semantic Layer；在 V2 重构后，本包同时承载：
- Layer 1/2：Raw/Staging/Normalize/Knowledge（保留的 legacy 管线）；
- Layer 3：History Backbone（backbone 子包，Source of Truth）；
- Layer 4：dist/ 产物构建与导出。

禁止从 Knowledge Store 自动推导 Event/Story；历史主干只能来自 Curated Backbone。
"""

from .database import SCHEMA_SQL, build_database

__all__ = ["SCHEMA_SQL", "build_database"]
