/** Mirrors backend `PlateBase` (src/plates/schemas.py). */
export interface Plate {
  label: string | null;
  code: string;
}

/** Full DB row, returned by create/update (backend `Plate` model). */
export interface PlateWithId extends Plate {
  id: string;
}

/** Paginated list payload (backend `PlatePublic`). */
export interface PlateList {
  data: Plate[];
  total: number;
  offset: number;
  limit: number;
}

/** Request body for create/update (backend `PlateCreate` / `PlateUpdate`). */
export interface PlateInput {
  label?: string | null;
  code: string;
}

/** Response of GET /plates/{code} when the plate is whitelisted. */
export interface CheckResult {
  message: string;
  data: PlateWithId;
}
