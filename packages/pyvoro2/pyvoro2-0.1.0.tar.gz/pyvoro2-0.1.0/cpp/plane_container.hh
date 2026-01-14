
#pragma once

#include <vector>
#include <tuple>
#include <unordered_map>
#include <cstdint>
#include <cmath>

#include "voro++.hh"

namespace pyvoro2 {

using namespace voro;

/** A conservative "plane-fraction" policy base.
 *
 * Voro++ computes the midplane displacement as:
 *   rs = 0.5 * |r_j - r_i|^2
 *
 * We want a plane at fraction t along (i -> j), which corresponds to:
 *   rs' = t * |r_j - r_i|^2 = (2 t) * rs
 *
 * To be conservative and avoid incorrect pruning, r_scale_check() always
 * returns true and never rejects candidates.
 */
class plane_policy_base : public radius_mono {
protected:
  int current_id = -1;
  double default_t = 0.5;

  inline void r_init(int ijk, int s) { (void)ijk; (void)s; current_id = -1; }
  inline double r_scale(double rs, int ijk, int q) { (void)ijk; (void)q; return rs; }

  inline bool r_scale_check(double &rs, double mrs, int ijk, int q) {
    (void)mrs;
    rs = r_scale(rs, ijk, q);
    return true;
  }

  inline bool r_ctest(double crs, double mrs) { (void)crs; (void)mrs; return false; }
};

class plane_from_radii_policy : public plane_policy_base {
public:
  double **ppr = nullptr;
  int **idp = nullptr;

  explicit plane_from_radii_policy(double default_t_) { default_t = default_t_; }

  inline void attach(double **p_, int **id_) { ppr = p_; idp = id_; }

protected:
  double current_R = 0.0;

  inline void r_init(int ijk, int s) {
    current_id = idp ? idp[ijk][s] : -1;
    current_R = ppr ? ppr[ijk][4 * s + 3] : 0.0;
  }

  inline double r_scale(double rs, int ijk, int q) {
    (void)ijk;
    double Rj = ppr ? ppr[ijk][4 * q + 3] : 0.0;
    double denom = current_R + Rj;
    double t = denom == 0.0 ? default_t : (current_R / denom);
    return (2.0 * t) * rs;
  }
};

class plane_matrix_policy : public plane_policy_base {
public:
  int **idp = nullptr;
  const double *matrix = nullptr;
  int n = 0;

  plane_matrix_policy(double default_t_, int n_, const double *matrix_)
    : matrix(matrix_), n(n_) {
    default_t = default_t_;
  }

  inline void attach(int **id_) { idp = id_; }

protected:
  inline void r_init(int ijk, int s) { current_id = idp ? idp[ijk][s] : -1; }

  inline double r_scale(double rs, int ijk, int q) {
    if (!idp || !matrix || current_id < 0) return rs;
    int j = idp[ijk][q];
    if (j < 0 || j >= n || current_id >= n) return (2.0 * default_t) * rs;
    double t = matrix[current_id * n + j];
    if (!std::isfinite(t)) t = default_t;
    if (t < 0.0) t = 0.0;
    if (t > 1.0) t = 1.0;
    return (2.0 * t) * rs;
  }
};

class plane_pairs_policy : public plane_policy_base {
public:
  int **idp = nullptr;
  inline void attach(int **id_) { idp = id_; }
  std::unordered_map<std::uint64_t, double> table;

  plane_pairs_policy(double default_t_, const std::vector<std::tuple<int, int, double>> &pairs) {
    default_t = default_t_;
    table.reserve(pairs.size() * 2);
    for (const auto &tup : pairs) {
      int i, j;
      double t;
      std::tie(i, j, t) = tup;
      std::uint64_t key = (static_cast<std::uint64_t>(static_cast<std::uint32_t>(i)) << 32)
                        | static_cast<std::uint32_t>(j);
      table[key] = t;
    }
  }
protected:
  inline void r_init(int ijk, int s) { current_id = idp ? idp[ijk][s] : -1; }

  inline double r_scale(double rs, int ijk, int q) {
    if (!idp || current_id < 0) return rs;
    int j = idp[ijk][q];
    std::uint64_t key = (static_cast<std::uint64_t>(static_cast<std::uint32_t>(current_id)) << 32)
                      | static_cast<std::uint32_t>(j);
    auto it = table.find(key);
    double t = (it == table.end()) ? default_t : it->second;
    if (!std::isfinite(t)) t = default_t;
    if (t < 0.0) t = 0.0;
    if (t > 1.0) t = 1.0;
    return (2.0 * t) * rs;
  }
};

// Non-periodic containers (Box domain)
class container_plane_from_radii : public container_base, public plane_from_radii_policy {
public:
  container_plane_from_radii(double ax_, double bx_, double ay_, double by_, double az_, double bz_,
                             int nx_, int ny_, int nz_, bool xper_, bool yper_, bool zper_,
                             int init_mem_, double default_t_);

  void clear();
  void put(int n, double x, double y, double z, double R);


  template <class v_cell, class c_loop>
  inline bool compute_cell(v_cell &c, c_loop &vl) {
    return vc.compute_cell(c, vl.ijk, vl.q, vl.i, vl.j, vl.k);
  }

private:
  voro_compute<container_plane_from_radii> vc;
  friend class voro_compute<container_plane_from_radii>;
};

class container_plane_matrix : public container_base, public plane_matrix_policy {
public:
  container_plane_matrix(double ax_, double bx_, double ay_, double by_, double az_, double bz_,
                         int nx_, int ny_, int nz_, bool xper_, bool yper_, bool zper_,
                         int init_mem_, double default_t_, int n_points_, const double *matrix_);

  void clear();
  void put(int n, double x, double y, double z, double R);


  template <class v_cell, class c_loop>
  inline bool compute_cell(v_cell &c, c_loop &vl) {
    return vc.compute_cell(c, vl.ijk, vl.q, vl.i, vl.j, vl.k);
  }

private:
  voro_compute<container_plane_matrix> vc;
  friend class voro_compute<container_plane_matrix>;
};

class container_plane_pairs : public container_base, public plane_pairs_policy {
public:
  container_plane_pairs(double ax_, double bx_, double ay_, double by_, double az_, double bz_,
                        int nx_, int ny_, int nz_, bool xper_, bool yper_, bool zper_,
                        int init_mem_, double default_t_, const std::vector<std::tuple<int, int, double>> &pairs);

  void clear();
  void put(int n, double x, double y, double z, double R);


  template <class v_cell, class c_loop>
  inline bool compute_cell(v_cell &c, c_loop &vl) {
    return vc.compute_cell(c, vl.ijk, vl.q, vl.i, vl.j, vl.k);
  }

private:
  voro_compute<container_plane_pairs> vc;
  friend class voro_compute<container_plane_pairs>;
};

// Periodic containers (triclinic cell)
class container_periodic_plane_from_radii : public container_periodic_base, public plane_from_radii_policy {
public:
  container_periodic_plane_from_radii(double bx_, double bxy_, double by_, double bxz_, double byz_, double bz_,
                                      int nx_, int ny_, int nz_, int init_mem_, double default_t_);

  void clear();
  void put(int n, double x, double y, double z, double R);


  template <class v_cell, class c_loop>
  inline bool compute_cell(v_cell &c, c_loop &vl) {
    return vc.compute_cell(c, vl.ijk, vl.q, vl.i, vl.j, vl.k);
  }

private:
  voro_compute<container_periodic_plane_from_radii> vc;
  friend class voro_compute<container_periodic_plane_from_radii>;
};

class container_periodic_plane_matrix : public container_periodic_base, public plane_matrix_policy {
public:
  container_periodic_plane_matrix(double bx_, double bxy_, double by_, double bxz_, double byz_, double bz_,
                                  int nx_, int ny_, int nz_, int init_mem_,
                                  double default_t_, int n_points_, const double *matrix_);

  void clear();
  void put(int n, double x, double y, double z, double R);


  template <class v_cell, class c_loop>
  inline bool compute_cell(v_cell &c, c_loop &vl) {
    return vc.compute_cell(c, vl.ijk, vl.q, vl.i, vl.j, vl.k);
  }

private:
  voro_compute<container_periodic_plane_matrix> vc;
  friend class voro_compute<container_periodic_plane_matrix>;
};

class container_periodic_plane_pairs : public container_periodic_base, public plane_pairs_policy {
public:
  container_periodic_plane_pairs(double bx_, double bxy_, double by_, double bxz_, double byz_, double bz_,
                                 int nx_, int ny_, int nz_, int init_mem_,
                                 double default_t_, const std::vector<std::tuple<int, int, double>> &pairs);

  void clear();
  void put(int n, double x, double y, double z, double R);


  template <class v_cell, class c_loop>
  inline bool compute_cell(v_cell &c, c_loop &vl) {
    return vc.compute_cell(c, vl.ijk, vl.q, vl.i, vl.j, vl.k);
  }

private:
  voro_compute<container_periodic_plane_pairs> vc;
  friend class voro_compute<container_periodic_plane_pairs>;
};

} // namespace pyvoro2
