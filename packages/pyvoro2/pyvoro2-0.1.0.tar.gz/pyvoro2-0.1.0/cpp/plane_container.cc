
#include "plane_container.hh"

namespace pyvoro2 {

using namespace voro;

// -------------------- Box (container_base) --------------------

container_plane_from_radii::container_plane_from_radii(
  double ax_, double bx_, double ay_, double by_, double az_, double bz_,
  int nx_, int ny_, int nz_, bool xper_, bool yper_, bool zper_,
  int init_mem_, double default_t_
) : container_base(ax_, bx_, ay_, by_, az_, bz_, nx_, ny_, nz_, xper_, yper_, zper_, init_mem_, 4),
	vc(*this, xper_?2*nx_+1:nx_, yper_?2*ny_+1:ny_, zper_?2*nz_+1:nz_),
	plane_from_radii_policy(default_t_) {
  attach(p, id);
}

void container_plane_from_radii::clear() {
  for (int *cop = co; cop < co + nxyz; cop++) *cop = 0;
}

void container_plane_from_radii::put(int n, double x, double y, double z, double R) {
  int ijk;
  if (put_locate_block(ijk, x, y, z)) {
    id[ijk][co[ijk]] = n;
    double *pp = p[ijk] + 4 * co[ijk]++;
    *(pp++) = x; *(pp++) = y; *(pp++) = z; *pp = R;
  }
}

container_plane_matrix::container_plane_matrix(
  double ax_, double bx_, double ay_, double by_, double az_, double bz_,
  int nx_, int ny_, int nz_, bool xper_, bool yper_, bool zper_,
  int init_mem_, double default_t_, int n_points_, const double *matrix_
) : container_base(ax_, bx_, ay_, by_, az_, bz_, nx_, ny_, nz_, xper_, yper_, zper_, init_mem_, 4),
	vc(*this, xper_?2*nx_+1:nx_, yper_?2*ny_+1:ny_, zper_?2*nz_+1:nz_),
	plane_matrix_policy(default_t_, n_points_, matrix_) {
  attach(id);
}

void container_plane_matrix::clear() {
  for (int *cop = co; cop < co + nxyz; cop++) *cop = 0;
}

void container_plane_matrix::put(int n, double x, double y, double z, double R) {
  (void)R;
  int ijk;
  if (put_locate_block(ijk, x, y, z)) {
    id[ijk][co[ijk]] = n;
    double *pp = p[ijk] + 4 * co[ijk]++;
    *(pp++) = x; *(pp++) = y; *(pp++) = z; *pp = 0.0;
  }
}

container_plane_pairs::container_plane_pairs(
  double ax_, double bx_, double ay_, double by_, double az_, double bz_,
  int nx_, int ny_, int nz_, bool xper_, bool yper_, bool zper_,
  int init_mem_, double default_t_, const std::vector<std::tuple<int, int, double>> &pairs
) : container_base(ax_, bx_, ay_, by_, az_, bz_, nx_, ny_, nz_, xper_, yper_, zper_, init_mem_, 4),
	vc(*this, xper_?2*nx_+1:nx_, yper_?2*ny_+1:ny_, zper_?2*nz_+1:nz_),
	plane_pairs_policy(default_t_, pairs) {
  attach(id);
}

void container_plane_pairs::clear() {
  for (int *cop = co; cop < co + nxyz; cop++) *cop = 0;
}

void container_plane_pairs::put(int n, double x, double y, double z, double R) {
  (void)R;
  int ijk;
  if (put_locate_block(ijk, x, y, z)) {
    id[ijk][co[ijk]] = n;
    double *pp = p[ijk] + 4 * co[ijk]++;
    *(pp++) = x; *(pp++) = y; *(pp++) = z; *pp = 0.0;
  }
}

// -------------------- Periodic (container_periodic_base) --------------------

container_periodic_plane_from_radii::container_periodic_plane_from_radii(
  double bx_, double bxy_, double by_, double bxz_, double byz_, double bz_,
  int nx_, int ny_, int nz_, int init_mem_, double default_t_
) : container_periodic_base(bx_, bxy_, by_, bxz_, byz_, bz_, nx_, ny_, nz_, init_mem_, 4),
	vc(*this, 2*nx_+1, 2*ey+1, 2*ez+1),
	plane_from_radii_policy(default_t_) {
  attach(p, id);
}

void container_periodic_plane_from_radii::clear() {
  for (int *cop = co; cop < co + oxyz; cop++) *cop = 0;
}

void container_periodic_plane_from_radii::put(int n, double x, double y, double z, double R) {
  int ijk;
  put_locate_block(ijk, x, y, z);
  for (int l = 0; l < co[ijk]; l++) check_duplicate(n, x, y, z, id[ijk][l], p[ijk] + 4 * l);
  id[ijk][co[ijk]] = n;
  double *pp = p[ijk] + 4 * co[ijk]++;
  *(pp++) = x; *(pp++) = y; *(pp++) = z; *pp = R;
}

container_periodic_plane_matrix::container_periodic_plane_matrix(
  double bx_, double bxy_, double by_, double bxz_, double byz_, double bz_,
  int nx_, int ny_, int nz_, int init_mem_,
  double default_t_, int n_points_, const double *matrix_
) : container_periodic_base(bx_, bxy_, by_, bxz_, byz_, bz_, nx_, ny_, nz_, init_mem_, 4),
	vc(*this, 2*nx_+1, 2*ey+1, 2*ez+1),
	plane_matrix_policy(default_t_, n_points_, matrix_) {
  attach(id);
}

void container_periodic_plane_matrix::clear() {
  for (int *cop = co; cop < co + oxyz; cop++) *cop = 0;
}

void container_periodic_plane_matrix::put(int n, double x, double y, double z, double R) {
  (void)R;
  int ijk;
  put_locate_block(ijk, x, y, z);
  for (int l = 0; l < co[ijk]; l++) check_duplicate(n, x, y, z, id[ijk][l], p[ijk] + 4 * l);
  id[ijk][co[ijk]] = n;
  double *pp = p[ijk] + 4 * co[ijk]++;
  *(pp++) = x; *(pp++) = y; *(pp++) = z; *pp = 0.0;
}

container_periodic_plane_pairs::container_periodic_plane_pairs(
  double bx_, double bxy_, double by_, double bxz_, double byz_, double bz_,
  int nx_, int ny_, int nz_, int init_mem_,
  double default_t_, const std::vector<std::tuple<int, int, double>> &pairs
) : container_periodic_base(bx_, bxy_, by_, bxz_, byz_, bz_, nx_, ny_, nz_, init_mem_, 4),
	vc(*this, 2*nx_+1, 2*ey+1, 2*ez+1),
	plane_pairs_policy(default_t_, pairs) {
  attach(id);
}

void container_periodic_plane_pairs::clear() {
  for (int *cop = co; cop < co + oxyz; cop++) *cop = 0;
}

void container_periodic_plane_pairs::put(int n, double x, double y, double z, double R) {
  (void)R;
  int ijk;
  put_locate_block(ijk, x, y, z);
  for (int l = 0; l < co[ijk]; l++) check_duplicate(n, x, y, z, id[ijk][l], p[ijk] + 4 * l);
  id[ijk][co[ijk]] = n;
  double *pp = p[ijk] + 4 * co[ijk]++;
  *(pp++) = x; *(pp++) = y; *(pp++) = z; *pp = 0.0;
}

} // namespace pyvoro2
