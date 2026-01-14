
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>

#include <vector>
#include <array>
#include <unordered_map>
#include <limits>
#include <cstddef>
#include <stdexcept>

#include "voro++.hh"
#include "plane_container.hh"

namespace py = pybind11;
using namespace voro;
using namespace pyvoro2;

namespace {

struct OutputOpts {
  bool vertices;
  bool adjacency;
  bool faces;
};

OutputOpts parse_opts(const std::tuple<bool, bool, bool>& opts) {
  return OutputOpts{std::get<0>(opts), std::get<1>(opts), std::get<2>(opts)};
}

py::dict build_cell_dict(voronoicell_neighbor& cell, int pid, double x, double y, double z, const OutputOpts& opts) {
  py::dict out;
  out["id"] = pid;
  out["volume"] = cell.volume();

  if (opts.vertices) {
    std::vector<double> positions;
    cell.vertices(x, y, z, positions);
    py::list verts;
    for (std::size_t i = 0; i + 2 < positions.size(); i += 3) {
      py::list v;
      v.append(positions[i]);
      v.append(positions[i + 1]);
      v.append(positions[i + 2]);
      verts.append(v);
    }
    out["vertices"] = verts;
  }

  if (opts.adjacency) {
    py::list adj;
    for (int i = 0; i < cell.p; i++) {
      py::list row;
      for (int j = 0; j < cell.nu[i]; j++) row.append(cell.ed[i][j]);
      adj.append(row);
    }
    out["adjacency"] = adj;
  }

  if (opts.faces) {
    std::vector<int> neigh;
    cell.neighbors(neigh);
    int num_faces = cell.number_of_faces();

    std::vector<int> fflat;
    cell.face_vertices(fflat);

    py::list faces;

    int k = 0;
    for (int i = 0; i < num_faces; i++) {
      if (k >= static_cast<int>(fflat.size())) {
        throw std::runtime_error("face_vertices encoding underflow");
      }
      int l = fflat[k++];
      if (l < 0) l = 0;
      if (k + l > static_cast<int>(fflat.size())) {
        throw std::runtime_error("face_vertices encoding overflow");
      }

      py::dict fd;
      fd["adjacent_cell"] = neigh[i];

      py::list fv;
      for (int j = 0; j < l; j++) {
        fv.append(fflat[k++]);
      }
      fd["vertices"] = fv;
      faces.append(fd);
    }

    out["faces"] = faces;
  }

  return out;
}

template <class ContainerT, class LoopT>
py::list compute_cells_impl(ContainerT& con, LoopT& loop, const OutputOpts& opts) {
  py::list cells;
  voronoicell_neighbor cell;

  if (loop.start()) do {
    if (con.compute_cell(cell, loop)) {
      int pid;
      double x, y, z, r;
      loop.pos(pid, x, y, z, r);
      cells.append(build_cell_dict(cell, pid, x, y, z, opts));
    }
  } while (loop.inc());

  return cells;
}

void check_points(const py::array_t<double>& points) {
  if (points.ndim() != 2 || points.shape(1) != 3) {
    throw py::value_error("points must have shape (n, 3)");
  }
}

void check_ids(const py::array_t<int>& ids, py::ssize_t n) {
  if (ids.ndim() != 1 || ids.shape(0) != n) {
    throw py::value_error("ids must have shape (n,)");
  }
}

void check_radii(const py::array_t<double>& radii, py::ssize_t n) {
  if (radii.ndim() != 1 || radii.shape(0) != n) {
    throw py::value_error("radii must have shape (n,)");
  }
}

} // namespace

PYBIND11_MODULE(_core, m) {
  m.doc() = "pyvoro2 core bindings (Voro++ + plane-fraction extensions)";

  m.def(
    "compute_box_standard",
    [](py::array_t<double, py::array::c_style | py::array::forcecast> points,
       py::array_t<int, py::array::c_style | py::array::forcecast> ids,
       std::array<std::array<double, 2>, 3> bounds,
       std::array<int, 3> blocks,
       int init_mem,
       std::tuple<bool, bool, bool> opts_tuple) {
      check_points(points);
      const auto n = points.shape(0);
      check_ids(ids, n);
      auto opts = parse_opts(opts_tuple);

      auto p = points.unchecked<2>();
      auto id = ids.unchecked<1>();

      container con(bounds[0][0], bounds[0][1],
                    bounds[1][0], bounds[1][1],
                    bounds[2][0], bounds[2][1],
                    blocks[0], blocks[1], blocks[2],
                    false, false, false, init_mem);

      for (py::ssize_t i = 0; i < n; i++) {
        con.put(id(i), p(i, 0), p(i, 1), p(i, 2));
      }

      c_loop_all loop(con);
      return compute_cells_impl(con, loop, opts);
    },
    py::arg("points"),
    py::arg("ids"),
    py::arg("bounds"),
    py::arg("blocks"),
    py::arg("init_mem"),
    py::arg("opts")
  );

  m.def(
    "compute_box_power",
    [](py::array_t<double, py::array::c_style | py::array::forcecast> points,
       py::array_t<int, py::array::c_style | py::array::forcecast> ids,
       py::array_t<double, py::array::c_style | py::array::forcecast> radii,
       std::array<std::array<double, 2>, 3> bounds,
       std::array<int, 3> blocks,
       int init_mem,
       std::tuple<bool, bool, bool> opts_tuple) {
      check_points(points);
      const auto n = points.shape(0);
      check_ids(ids, n);
      check_radii(radii, n);
      auto opts = parse_opts(opts_tuple);

      auto p = points.unchecked<2>();
      auto id = ids.unchecked<1>();
      auto r = radii.unchecked<1>();

      container_poly con(bounds[0][0], bounds[0][1],
                         bounds[1][0], bounds[1][1],
                         bounds[2][0], bounds[2][1],
                         blocks[0], blocks[1], blocks[2],
                         false, false, false, init_mem);

      for (py::ssize_t i = 0; i < n; i++) {
        con.put(id(i), p(i, 0), p(i, 1), p(i, 2), r(i));
      }

      c_loop_all loop(con);
      return compute_cells_impl(con, loop, opts);
    },
    py::arg("points"),
    py::arg("ids"),
    py::arg("radii"),
    py::arg("bounds"),
    py::arg("blocks"),
    py::arg("init_mem"),
    py::arg("opts")
  );

  m.def(
    "compute_box_plane_from_radii",
    [](py::array_t<double, py::array::c_style | py::array::forcecast> points,
       py::array_t<int, py::array::c_style | py::array::forcecast> ids,
       py::array_t<double, py::array::c_style | py::array::forcecast> radii,
       double default_t,
       std::array<std::array<double, 2>, 3> bounds,
       std::array<int, 3> blocks,
       int init_mem,
       std::tuple<bool, bool, bool> opts_tuple) {
      check_points(points);
      const auto n = points.shape(0);
      check_ids(ids, n);
      check_radii(radii, n);
      auto opts = parse_opts(opts_tuple);

      auto p = points.unchecked<2>();
      auto id = ids.unchecked<1>();
      auto r = radii.unchecked<1>();

      container_plane_from_radii con(
        bounds[0][0], bounds[0][1],
        bounds[1][0], bounds[1][1],
        bounds[2][0], bounds[2][1],
        blocks[0], blocks[1], blocks[2],
        false, false, false, init_mem, default_t
      );

      for (py::ssize_t i = 0; i < n; i++) {
        con.put(id(i), p(i, 0), p(i, 1), p(i, 2), r(i));
      }

      c_loop_all loop(con);
      return compute_cells_impl(con, loop, opts);
    },
    py::arg("points"),
    py::arg("ids"),
    py::arg("radii"),
    py::arg("default_t"),
    py::arg("bounds"),
    py::arg("blocks"),
    py::arg("init_mem"),
    py::arg("opts")
  );

  m.def(
    "compute_box_plane_matrix",
    [](py::array_t<double, py::array::c_style | py::array::forcecast> points,
       py::array_t<int, py::array::c_style | py::array::forcecast> ids,
       py::array_t<double, py::array::c_style | py::array::forcecast> matrix,
       double default_t,
       std::array<std::array<double, 2>, 3> bounds,
       std::array<int, 3> blocks,
       int init_mem,
       std::tuple<bool, bool, bool> opts_tuple) {
      check_points(points);
      const auto n = points.shape(0);
      check_ids(ids, n);
      if (matrix.ndim() != 2 || matrix.shape(0) != n || matrix.shape(1) != n) {
        throw py::value_error("matrix must have shape (n, n)");
      }
      auto opts = parse_opts(opts_tuple);

      auto p = points.unchecked<2>();
      auto id = ids.unchecked<1>();
      auto t = matrix.unchecked<2>();

      container_plane_matrix con(
        bounds[0][0], bounds[0][1],
        bounds[1][0], bounds[1][1],
        bounds[2][0], bounds[2][1],
        blocks[0], blocks[1], blocks[2],
        false, false, false, init_mem, default_t,
        static_cast<int>(n),
        t.data(0, 0)
      );

      for (py::ssize_t i = 0; i < n; i++) {
        con.put(id(i), p(i, 0), p(i, 1), p(i, 2), 0.0);
      }

      c_loop_all loop(con);
      return compute_cells_impl(con, loop, opts);
    },
    py::arg("points"),
    py::arg("ids"),
    py::arg("matrix"),
    py::arg("default_t"),
    py::arg("bounds"),
    py::arg("blocks"),
    py::arg("init_mem"),
    py::arg("opts")
  );

  m.def(
    "compute_box_plane_pairs",
    [](py::array_t<double, py::array::c_style | py::array::forcecast> points,
       py::array_t<int, py::array::c_style | py::array::forcecast> ids,
       std::vector<std::tuple<int, int, double>> pairs,
       double default_t,
       std::array<std::array<double, 2>, 3> bounds,
       std::array<int, 3> blocks,
       int init_mem,
       std::tuple<bool, bool, bool> opts_tuple) {
      check_points(points);
      const auto n = points.shape(0);
      check_ids(ids, n);
      auto opts = parse_opts(opts_tuple);

      auto p = points.unchecked<2>();
      auto id = ids.unchecked<1>();

      container_plane_pairs con(
        bounds[0][0], bounds[0][1],
        bounds[1][0], bounds[1][1],
        bounds[2][0], bounds[2][1],
        blocks[0], blocks[1], blocks[2],
        false, false, false, init_mem, default_t,
        pairs
      );

      for (py::ssize_t i = 0; i < n; i++) {
        con.put(id(i), p(i, 0), p(i, 1), p(i, 2), 0.0);
      }

      c_loop_all loop(con);
      return compute_cells_impl(con, loop, opts);
    },
    py::arg("points"),
    py::arg("ids"),
    py::arg("pairs"),
    py::arg("default_t"),
    py::arg("bounds"),
    py::arg("blocks"),
    py::arg("init_mem"),
    py::arg("opts")
  );

  // Periodic cell variants
  m.def(
    "compute_periodic_standard",
    [](py::array_t<double, py::array::c_style | py::array::forcecast> points,
       py::array_t<int, py::array::c_style | py::array::forcecast> ids,
       std::array<double, 6> cell_params,
       std::array<int, 3> blocks,
       int init_mem,
       std::tuple<bool, bool, bool> opts_tuple) {
      check_points(points);
      const auto n = points.shape(0);
      check_ids(ids, n);
      auto opts = parse_opts(opts_tuple);

      auto p = points.unchecked<2>();
      auto id = ids.unchecked<1>();

      container_periodic con(cell_params[0], cell_params[1], cell_params[2],
                             cell_params[3], cell_params[4], cell_params[5],
                             blocks[0], blocks[1], blocks[2], init_mem);

      for (py::ssize_t i = 0; i < n; i++) {
        con.put(id(i), p(i, 0), p(i, 1), p(i, 2));
      }

      c_loop_all_periodic loop(con);
      return compute_cells_impl(con, loop, opts);
    },
    py::arg("points"),
    py::arg("ids"),
    py::arg("cell_params"),
    py::arg("blocks"),
    py::arg("init_mem"),
    py::arg("opts")
  );

  m.def(
    "compute_periodic_power",
    [](py::array_t<double, py::array::c_style | py::array::forcecast> points,
       py::array_t<int, py::array::c_style | py::array::forcecast> ids,
       py::array_t<double, py::array::c_style | py::array::forcecast> radii,
       std::array<double, 6> cell_params,
       std::array<int, 3> blocks,
       int init_mem,
       std::tuple<bool, bool, bool> opts_tuple) {
      check_points(points);
      const auto n = points.shape(0);
      check_ids(ids, n);
      check_radii(radii, n);
      auto opts = parse_opts(opts_tuple);

      auto p = points.unchecked<2>();
      auto id = ids.unchecked<1>();
      auto r = radii.unchecked<1>();

      container_periodic_poly con(cell_params[0], cell_params[1], cell_params[2],
                                  cell_params[3], cell_params[4], cell_params[5],
                                  blocks[0], blocks[1], blocks[2], init_mem);

      for (py::ssize_t i = 0; i < n; i++) {
        con.put(id(i), p(i, 0), p(i, 1), p(i, 2), r(i));
      }

      c_loop_all_periodic loop(con);
      return compute_cells_impl(con, loop, opts);
    },
    py::arg("points"),
    py::arg("ids"),
    py::arg("radii"),
    py::arg("cell_params"),
    py::arg("blocks"),
    py::arg("init_mem"),
    py::arg("opts")
  );

  m.def(
    "compute_periodic_plane_from_radii",
    [](py::array_t<double, py::array::c_style | py::array::forcecast> points,
       py::array_t<int, py::array::c_style | py::array::forcecast> ids,
       py::array_t<double, py::array::c_style | py::array::forcecast> radii,
       double default_t,
       std::array<double, 6> cell_params,
       std::array<int, 3> blocks,
       int init_mem,
       std::tuple<bool, bool, bool> opts_tuple) {
      check_points(points);
      const auto n = points.shape(0);
      check_ids(ids, n);
      check_radii(radii, n);
      auto opts = parse_opts(opts_tuple);

      auto p = points.unchecked<2>();
      auto id = ids.unchecked<1>();
      auto r = radii.unchecked<1>();

      container_periodic_plane_from_radii con(cell_params[0], cell_params[1], cell_params[2],
                                              cell_params[3], cell_params[4], cell_params[5],
                                              blocks[0], blocks[1], blocks[2], init_mem, default_t);

      for (py::ssize_t i = 0; i < n; i++) {
        con.put(id(i), p(i, 0), p(i, 1), p(i, 2), r(i));
      }

      c_loop_all_periodic loop(con);
      return compute_cells_impl(con, loop, opts);
    },
    py::arg("points"),
    py::arg("ids"),
    py::arg("radii"),
    py::arg("default_t"),
    py::arg("cell_params"),
    py::arg("blocks"),
    py::arg("init_mem"),
    py::arg("opts")
  );

  m.def(
    "compute_periodic_plane_matrix",
    [](py::array_t<double, py::array::c_style | py::array::forcecast> points,
       py::array_t<int, py::array::c_style | py::array::forcecast> ids,
       py::array_t<double, py::array::c_style | py::array::forcecast> matrix,
       double default_t,
       std::array<double, 6> cell_params,
       std::array<int, 3> blocks,
       int init_mem,
       std::tuple<bool, bool, bool> opts_tuple) {
      check_points(points);
      const auto n = points.shape(0);
      check_ids(ids, n);
      if (matrix.ndim() != 2 || matrix.shape(0) != n || matrix.shape(1) != n) {
        throw py::value_error("matrix must have shape (n, n)");
      }
      auto opts = parse_opts(opts_tuple);

      auto p = points.unchecked<2>();
      auto id = ids.unchecked<1>();
      auto t = matrix.unchecked<2>();

      container_periodic_plane_matrix con(cell_params[0], cell_params[1], cell_params[2],
                                          cell_params[3], cell_params[4], cell_params[5],
                                          blocks[0], blocks[1], blocks[2], init_mem, default_t,
                                          static_cast<int>(n), t.data(0, 0));

      for (py::ssize_t i = 0; i < n; i++) {
        con.put(id(i), p(i, 0), p(i, 1), p(i, 2), 0.0);
      }

      c_loop_all_periodic loop(con);
      return compute_cells_impl(con, loop, opts);
    },
    py::arg("points"),
    py::arg("ids"),
    py::arg("matrix"),
    py::arg("default_t"),
    py::arg("cell_params"),
    py::arg("blocks"),
    py::arg("init_mem"),
    py::arg("opts")
  );

  m.def(
    "compute_periodic_plane_pairs",
    [](py::array_t<double, py::array::c_style | py::array::forcecast> points,
       py::array_t<int, py::array::c_style | py::array::forcecast> ids,
       std::vector<std::tuple<int, int, double>> pairs,
       double default_t,
       std::array<double, 6> cell_params,
       std::array<int, 3> blocks,
       int init_mem,
       std::tuple<bool, bool, bool> opts_tuple) {
      check_points(points);
      const auto n = points.shape(0);
      check_ids(ids, n);
      auto opts = parse_opts(opts_tuple);

      auto p = points.unchecked<2>();
      auto id = ids.unchecked<1>();

      container_periodic_plane_pairs con(cell_params[0], cell_params[1], cell_params[2],
                                         cell_params[3], cell_params[4], cell_params[5],
                                         blocks[0], blocks[1], blocks[2], init_mem, default_t,
                                         pairs);

      for (py::ssize_t i = 0; i < n; i++) {
        con.put(id(i), p(i, 0), p(i, 1), p(i, 2), 0.0);
      }

      c_loop_all_periodic loop(con);
      return compute_cells_impl(con, loop, opts);
    },
    py::arg("points"),
    py::arg("ids"),
    py::arg("pairs"),
    py::arg("default_t"),
    py::arg("cell_params"),
    py::arg("blocks"),
    py::arg("init_mem"),
    py::arg("opts")
  );
}