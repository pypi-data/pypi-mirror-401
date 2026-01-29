import { computed as _e, watch as Zt, defineComponent as we, useTemplateRef as Ae, shallowRef as Oe, onMounted as je, useAttrs as Ie, createElementBlock as Se, openBlock as Ce, mergeProps as Me, unref as Ee } from "vue";
import * as qt from "echarts";
import { useBindingGetter as Te } from "instaui";
function* q(t, e, n) {
  if (!e || n === "value") {
    yield void 0;
    return;
  }
  const r = t.dimensions.indexOf(e);
  if (r === -1) throw new Error(`Invalid color field: ${e}`);
  const o = /* @__PURE__ */ new Set();
  for (const i of t.source) {
    const a = i[r];
    o.has(a) || (o.add(a), yield a);
  }
}
function J(t, e) {
  return {
    labelConfig: t ? e : void 0,
    encodeLabelConfig: t ? {
      label: t
    } : void 0
  };
}
function U(t) {
  return {
    encodeTooltipConfig: t ? {
      tooltip: t
    } : void 0
  };
}
function I(t) {
  const { dataset: e, field: n } = t, r = e.dimensions.indexOf(n);
  if (r === -1)
    throw new Error(`Invalid color field: ${n}`);
  return typeof e.source[0][r] == "string" ? "category" : "value";
}
function $e(t) {
  const { dataset: e, field: n } = t, r = e.dimensions.indexOf(n);
  if (r === -1)
    throw new Error(`Invalid color field: ${n}`);
  const o = e.source.map((s) => s[r]), i = Math.min(...o), a = Math.max(...o);
  return [i, a];
}
function X(t) {
  const { xType: e, xField: n, extendConfig: r } = t;
  return { ...r, type: e, name: n + " →" };
}
function G(t) {
  const { yType: e, yField: n, extendConfig: r } = t;
  return { ...r, type: e, name: "↑ " + n };
}
function Jt(t) {
  const { colorField: e, colorValue: n } = t;
  if (e)
    return n;
}
class yt {
  constructor(e) {
    this.dataset = e;
  }
  filterWithFacet(e) {
    const { facetConfig: n, rowValue: r, columnValue: o } = e, i = this.dataset.dimensions, a = this.dataset.source, { row: s, column: c } = n, l = s ? i.indexOf(s) : -1, u = c ? i.indexOf(c) : -1, f = {
      source: l > -1 || u > -1 ? a.filter((d) => {
        const p = l === -1 || r === void 0 || d[l] === r, y = u === -1 || o === void 0 || d[u] === o;
        return p && y;
      }) : a,
      dimensions: i
    };
    return new yt(f);
  }
  getValues(e) {
    const n = this.dataset.dimensions.indexOf(e);
    if (n === -1)
      throw new Error(`Invalid field: ${e}`);
    return this.dataset.source.map((r) => r[n]);
  }
}
const gt = {
  axisLine: {
    show: !1
  }
}, mt = {
  axisLine: {
    show: !1
  }
}, ze = {
  axisLine: {
    show: !1,
    onZero: !1
  }
}, Fe = {
  axisLine: {
    show: !1,
    onZero: !1
  }
};
function Pe(t, e, n) {
  const r = t.x || "x", o = t.y || "y", i = t.color, a = t.echarts || {}, { facetInfo: s } = e, { row: c, column: l } = t.facet || {}, u = c !== void 0, f = l !== void 0, d = i ? I({
    dataset: t.data,
    field: i
  }) : void 0;
  s.rowValues.forEach((p) => {
    s.columnValues.forEach((y) => {
      const x = n.getAxes({
        rowValue: p,
        columnValue: y
      }), A = x.fillXAxisConfig({
        config: X({
          xType: "category",
          xField: r,
          extendConfig: gt
        }),
        xName: r
      }), b = x.fillYAxisConfig({
        config: G({
          yType: "value",
          yField: o,
          extendConfig: mt
        }),
        yName: o
      });
      for (const _ of q(
        t.data,
        i,
        d
      )) {
        const g = [];
        u && g.push({ dim: c, value: p }), f && g.push({ dim: l, value: y }), i && d === "category" && g.push({ dim: i, value: _ });
        const { labelConfig: S, encodeLabelConfig: O } = J(
          t.label,
          {
            label: {
              show: !0,
              position: "insideTop"
            }
          }
        ), { encodeTooltipConfig: m } = U(
          t.tooltip
        ), v = {
          ...a,
          type: "bar",
          ...S,
          encode: { x: r, y: o, ...O, ...m },
          datasetId: n.datasetManager.getDatasetId({
            data: t.data,
            filters: g
          }),
          xAxisId: A,
          yAxisId: b
        };
        n.addSeries(v);
      }
    });
  });
}
function Ve(t, e, n) {
  const r = t.x || "x", o = t.y || "y", i = t.color, { facetInfo: a } = e, { row: s, column: c } = t.facet || {}, l = t.echarts || {}, u = s !== void 0, f = c !== void 0, d = i ? I({
    dataset: t.data,
    field: i
  }) : void 0;
  a.rowValues.forEach((p) => {
    a.columnValues.forEach((y) => {
      const x = n.getAxes({
        rowValue: p,
        columnValue: y
      }), A = x.fillXAxisConfig({
        config: X({
          xType: "category",
          xField: r,
          extendConfig: gt
        }),
        xName: r
      }), b = x.fillYAxisConfig({
        config: G({
          yType: "value",
          yField: o,
          extendConfig: mt
        }),
        yName: o
      });
      for (const _ of q(
        t.data,
        i,
        d
      )) {
        const g = [];
        u && g.push({ dim: s, value: p }), f && g.push({ dim: c, value: y }), i && d === "category" && g.push({ dim: i, value: _ });
        const { labelConfig: S, encodeLabelConfig: O } = J(
          t.label,
          {
            label: {
              show: !0,
              position: "top"
            }
          }
        ), { encodeTooltipConfig: m } = U(
          t.tooltip
        ), v = {
          ...l,
          type: "line",
          showSymbol: !1,
          ...S,
          encode: { x: r, y: o, ...O, ...m },
          datasetId: n.datasetManager.getDatasetId({
            data: t.data,
            filters: g
          }),
          xAxisId: A,
          yAxisId: b
        };
        n.addSeries(v);
      }
    });
  });
}
function Ne(t, e, n) {
  const { facetInfo: r } = e, { row: o, column: i } = t.facet || {}, a = t.echarts || {}, s = o !== void 0, c = i !== void 0;
  r.rowValues.forEach((l) => {
    r.columnValues.forEach((u) => {
      const f = [];
      s && f.push({ dim: o, value: l }), c && f.push({ dim: i, value: u });
      const { encodeTooltipConfig: d } = U(
        t.tooltip
      ), p = {
        ...a,
        type: "pie",
        encode: {
          name: t.name || "name",
          value: t.value || "value",
          ...d
        },
        datasetId: n.datasetManager.getDatasetId({
          data: t.data,
          filters: f
        })
      };
      n.addSeries(p);
    });
  });
}
function De(t, e, n) {
  const r = t.x || "x", o = t.y || "y", i = t.color, a = t.size, { facetInfo: s } = e, { row: c, column: l } = t.facet || {}, u = t.echarts || {}, f = c !== void 0, d = l !== void 0, p = i ? I({
    dataset: t.data,
    field: i
  }) : void 0, y = i ? $e({
    dataset: t.data,
    field: i
  }) : void 0, x = I({
    dataset: t.data,
    field: r
  }), A = I({
    dataset: t.data,
    field: o
  });
  s.rowValues.forEach((b) => {
    s.columnValues.forEach((_) => {
      const g = n.getAxes({
        rowValue: b,
        columnValue: _
      }), S = g.fillXAxisConfig({
        config: X({
          xType: x,
          xField: r,
          extendConfig: ze
        }),
        xName: r
      }), O = g.fillYAxisConfig({
        config: G({
          yType: A,
          yField: o,
          extendConfig: Fe
        }),
        yName: o
      });
      for (const m of q(
        t.data,
        i,
        p
      )) {
        const v = [];
        f && v.push({ dim: c, value: b }), d && v.push({ dim: l, value: _ }), i && p === "category" && v.push({ dim: i, value: m });
        const { labelConfig: it, encodeLabelConfig: at } = J(
          t.label,
          {
            label: {
              show: !0,
              position: "top"
            }
          }
        ), { encodeTooltipConfig: st } = U(
          t.tooltip
        ), ct = {
          name: Jt({ colorField: i, colorValue: m }),
          ...u,
          type: "scatter",
          ...it,
          encode: { x: r, y: o, ...at, ...st },
          datasetId: n.datasetManager.getDatasetId({
            data: t.data,
            filters: v
          }),
          xAxisId: S,
          yAxisId: O
        }, Ct = n.addSeries(ct);
        a && n.addVisualMap({
          show: !1,
          type: "continuous",
          seriesId: Ct,
          dimension: a,
          inRange: {
            symbolSize: [10, 100]
          }
        }), i && p === "value" && n.addVisualMap({
          show: !1,
          type: "continuous",
          min: y[0],
          max: y[1],
          seriesId: Ct,
          dimension: i,
          inRange: {
            color: ["#053061", "#f4eeeb", "#67001f"]
          }
        });
      }
    });
  });
}
function Re(t, e, n) {
  const r = t.x || "x", o = t.y || "y", i = t.color, a = t.size, { facetInfo: s } = e, { row: c, column: l } = t.facet || {}, u = t.echarts || {}, f = c !== void 0, d = l !== void 0, p = i ? I({
    dataset: t.data,
    field: i
  }) : void 0, y = I({
    dataset: t.data,
    field: r
  }), x = I({
    dataset: t.data,
    field: o
  });
  s.rowValues.forEach((A) => {
    s.columnValues.forEach((b) => {
      const _ = n.getAxes({
        rowValue: A,
        columnValue: b
      }), g = _.fillXAxisConfig({
        config: X({ xType: y, xField: r }),
        xName: r
      }), S = _.fillYAxisConfig({
        config: G({ yType: x, yField: o }),
        yName: o
      });
      for (const O of q(
        t.data,
        i,
        p
      )) {
        const m = [];
        f && m.push({ dim: c, value: A }), d && m.push({ dim: l, value: b }), i && p === "category" && m.push({ dim: i, value: O });
        const { labelConfig: v, encodeLabelConfig: it } = J(
          t.label,
          {
            label: {
              show: !0,
              position: "top"
            }
          }
        ), { encodeTooltipConfig: at } = U(
          t.tooltip
        ), st = {
          name: Jt({ colorField: i, colorValue: O }),
          ...u,
          type: "effectScatter",
          ...v,
          encode: { x: r, y: o, ...it, ...at },
          datasetId: n.datasetManager.getDatasetId({
            data: t.data,
            filters: m
          }),
          xAxisId: g,
          yAxisId: S
        }, ct = n.addSeries(st);
        a && n.addVisualMap({
          show: !1,
          type: "continuous",
          seriesId: ct,
          dimension: a,
          inRange: {
            symbolSize: [10, 100]
          }
        });
      }
    });
  });
}
var Qt = typeof global == "object" && global && global.Object === Object && global, We = typeof self == "object" && self && self.Object === Object && self, z = Qt || We || Function("return this")(), B = z.Symbol, te = Object.prototype, Le = te.hasOwnProperty, Ue = te.toString, N = B ? B.toStringTag : void 0;
function Xe(t) {
  var e = Le.call(t, N), n = t[N];
  try {
    t[N] = void 0;
    var r = !0;
  } catch {
  }
  var o = Ue.call(t);
  return r && (e ? t[N] = n : delete t[N]), o;
}
var Ge = Object.prototype, He = Ge.toString;
function Be(t) {
  return He.call(t);
}
var Ye = "[object Null]", ke = "[object Undefined]", Mt = B ? B.toStringTag : void 0;
function Q(t) {
  return t == null ? t === void 0 ? ke : Ye : Mt && Mt in Object(t) ? Xe(t) : Be(t);
}
function H(t) {
  return t != null && typeof t == "object";
}
var Y = Array.isArray;
function E(t) {
  var e = typeof t;
  return t != null && (e == "object" || e == "function");
}
function ee(t) {
  return t;
}
var Ke = "[object AsyncFunction]", Ze = "[object Function]", qe = "[object GeneratorFunction]", Je = "[object Proxy]";
function vt(t) {
  if (!E(t))
    return !1;
  var e = Q(t);
  return e == Ze || e == qe || e == Ke || e == Je;
}
var ut = z["__core-js_shared__"], Et = function() {
  var t = /[^.]+$/.exec(ut && ut.keys && ut.keys.IE_PROTO || "");
  return t ? "Symbol(src)_1." + t : "";
}();
function Qe(t) {
  return !!Et && Et in t;
}
var tn = Function.prototype, en = tn.toString;
function nn(t) {
  if (t != null) {
    try {
      return en.call(t);
    } catch {
    }
    try {
      return t + "";
    } catch {
    }
  }
  return "";
}
var rn = /[\\^$.*+?()[\]{}|]/g, on = /^\[object .+?Constructor\]$/, an = Function.prototype, sn = Object.prototype, cn = an.toString, un = sn.hasOwnProperty, ln = RegExp(
  "^" + cn.call(un).replace(rn, "\\$&").replace(/hasOwnProperty|(function).*?(?=\\\()| for .+?(?=\\\])/g, "$1.*?") + "$"
);
function fn(t) {
  if (!E(t) || Qe(t))
    return !1;
  var e = vt(t) ? ln : on;
  return e.test(nn(t));
}
function dn(t, e) {
  return t?.[e];
}
function xt(t, e) {
  var n = dn(t, e);
  return fn(n) ? n : void 0;
}
var Tt = Object.create, pn = /* @__PURE__ */ function() {
  function t() {
  }
  return function(e) {
    if (!E(e))
      return {};
    if (Tt)
      return Tt(e);
    t.prototype = e;
    var n = new t();
    return t.prototype = void 0, n;
  };
}();
function hn(t, e, n) {
  switch (n.length) {
    case 0:
      return t.call(e);
    case 1:
      return t.call(e, n[0]);
    case 2:
      return t.call(e, n[0], n[1]);
    case 3:
      return t.call(e, n[0], n[1], n[2]);
  }
  return t.apply(e, n);
}
function yn(t, e) {
  var n = -1, r = t.length;
  for (e || (e = Array(r)); ++n < r; )
    e[n] = t[n];
  return e;
}
var gn = 800, mn = 16, vn = Date.now;
function xn(t) {
  var e = 0, n = 0;
  return function() {
    var r = vn(), o = mn - (r - n);
    if (n = r, o > 0) {
      if (++e >= gn)
        return arguments[0];
    } else
      e = 0;
    return t.apply(void 0, arguments);
  };
}
function bn(t) {
  return function() {
    return t;
  };
}
var k = function() {
  try {
    var t = xt(Object, "defineProperty");
    return t({}, "", {}), t;
  } catch {
  }
}(), _n = k ? function(t, e) {
  return k(t, "toString", {
    configurable: !0,
    enumerable: !1,
    value: bn(e),
    writable: !0
  });
} : ee, wn = xn(_n), An = 9007199254740991, On = /^(?:0|[1-9]\d*)$/;
function ne(t, e) {
  var n = typeof t;
  return e = e ?? An, !!e && (n == "number" || n != "symbol" && On.test(t)) && t > -1 && t % 1 == 0 && t < e;
}
function bt(t, e, n) {
  e == "__proto__" && k ? k(t, e, {
    configurable: !0,
    enumerable: !0,
    value: n,
    writable: !0
  }) : t[e] = n;
}
function tt(t, e) {
  return t === e || t !== t && e !== e;
}
var jn = Object.prototype, In = jn.hasOwnProperty;
function Sn(t, e, n) {
  var r = t[e];
  (!(In.call(t, e) && tt(r, n)) || n === void 0 && !(e in t)) && bt(t, e, n);
}
function Cn(t, e, n, r) {
  var o = !n;
  n || (n = {});
  for (var i = -1, a = e.length; ++i < a; ) {
    var s = e[i], c = void 0;
    c === void 0 && (c = t[s]), o ? bt(n, s, c) : Sn(n, s, c);
  }
  return n;
}
var $t = Math.max;
function Mn(t, e, n) {
  return e = $t(e === void 0 ? t.length - 1 : e, 0), function() {
    for (var r = arguments, o = -1, i = $t(r.length - e, 0), a = Array(i); ++o < i; )
      a[o] = r[e + o];
    o = -1;
    for (var s = Array(e + 1); ++o < e; )
      s[o] = r[o];
    return s[e] = n(a), hn(t, this, s);
  };
}
function En(t, e) {
  return wn(Mn(t, e, ee), t + "");
}
var Tn = 9007199254740991;
function re(t) {
  return typeof t == "number" && t > -1 && t % 1 == 0 && t <= Tn;
}
function _t(t) {
  return t != null && re(t.length) && !vt(t);
}
function $n(t, e, n) {
  if (!E(n))
    return !1;
  var r = typeof e;
  return (r == "number" ? _t(n) && ne(e, n.length) : r == "string" && e in n) ? tt(n[e], t) : !1;
}
function oe(t) {
  return En(function(e, n) {
    var r = -1, o = n.length, i = o > 1 ? n[o - 1] : void 0, a = o > 2 ? n[2] : void 0;
    for (i = t.length > 3 && typeof i == "function" ? (o--, i) : void 0, a && $n(n[0], n[1], a) && (i = o < 3 ? void 0 : i, o = 1), e = Object(e); ++r < o; ) {
      var s = n[r];
      s && t(e, s, r, i);
    }
    return e;
  });
}
var zn = Object.prototype;
function ie(t) {
  var e = t && t.constructor, n = typeof e == "function" && e.prototype || zn;
  return t === n;
}
function Fn(t, e) {
  for (var n = -1, r = Array(t); ++n < t; )
    r[n] = e(n);
  return r;
}
var Pn = "[object Arguments]";
function zt(t) {
  return H(t) && Q(t) == Pn;
}
var ae = Object.prototype, Vn = ae.hasOwnProperty, Nn = ae.propertyIsEnumerable, dt = zt(/* @__PURE__ */ function() {
  return arguments;
}()) ? zt : function(t) {
  return H(t) && Vn.call(t, "callee") && !Nn.call(t, "callee");
};
function Dn() {
  return !1;
}
var se = typeof exports == "object" && exports && !exports.nodeType && exports, Ft = se && typeof module == "object" && module && !module.nodeType && module, Rn = Ft && Ft.exports === se, Pt = Rn ? z.Buffer : void 0, Wn = Pt ? Pt.isBuffer : void 0, ce = Wn || Dn, Ln = "[object Arguments]", Un = "[object Array]", Xn = "[object Boolean]", Gn = "[object Date]", Hn = "[object Error]", Bn = "[object Function]", Yn = "[object Map]", kn = "[object Number]", Kn = "[object Object]", Zn = "[object RegExp]", qn = "[object Set]", Jn = "[object String]", Qn = "[object WeakMap]", tr = "[object ArrayBuffer]", er = "[object DataView]", nr = "[object Float32Array]", rr = "[object Float64Array]", or = "[object Int8Array]", ir = "[object Int16Array]", ar = "[object Int32Array]", sr = "[object Uint8Array]", cr = "[object Uint8ClampedArray]", ur = "[object Uint16Array]", lr = "[object Uint32Array]", h = {};
h[nr] = h[rr] = h[or] = h[ir] = h[ar] = h[sr] = h[cr] = h[ur] = h[lr] = !0;
h[Ln] = h[Un] = h[tr] = h[Xn] = h[er] = h[Gn] = h[Hn] = h[Bn] = h[Yn] = h[kn] = h[Kn] = h[Zn] = h[qn] = h[Jn] = h[Qn] = !1;
function fr(t) {
  return H(t) && re(t.length) && !!h[Q(t)];
}
function dr(t) {
  return function(e) {
    return t(e);
  };
}
var ue = typeof exports == "object" && exports && !exports.nodeType && exports, R = ue && typeof module == "object" && module && !module.nodeType && module, pr = R && R.exports === ue, lt = pr && Qt.process, Vt = function() {
  try {
    var t = R && R.require && R.require("util").types;
    return t || lt && lt.binding && lt.binding("util");
  } catch {
  }
}(), Nt = Vt && Vt.isTypedArray, le = Nt ? dr(Nt) : fr;
function hr(t, e) {
  var n = Y(t), r = !n && dt(t), o = !n && !r && ce(t), i = !n && !r && !o && le(t), a = n || r || o || i, s = a ? Fn(t.length, String) : [], c = s.length;
  for (var l in t)
    a && // Safari 9 has enumerable `arguments.length` in strict mode.
    (l == "length" || // Node.js 0.10 has enumerable non-index properties on buffers.
    o && (l == "offset" || l == "parent") || // PhantomJS 2 has enumerable non-index properties on typed arrays.
    i && (l == "buffer" || l == "byteLength" || l == "byteOffset") || // Skip index properties.
    ne(l, c)) || s.push(l);
  return s;
}
function yr(t, e) {
  return function(n) {
    return t(e(n));
  };
}
function gr(t) {
  var e = [];
  if (t != null)
    for (var n in Object(t))
      e.push(n);
  return e;
}
var mr = Object.prototype, vr = mr.hasOwnProperty;
function xr(t) {
  if (!E(t))
    return gr(t);
  var e = ie(t), n = [];
  for (var r in t)
    r == "constructor" && (e || !vr.call(t, r)) || n.push(r);
  return n;
}
function fe(t) {
  return _t(t) ? hr(t) : xr(t);
}
var W = xt(Object, "create");
function br() {
  this.__data__ = W ? W(null) : {}, this.size = 0;
}
function _r(t) {
  var e = this.has(t) && delete this.__data__[t];
  return this.size -= e ? 1 : 0, e;
}
var wr = "__lodash_hash_undefined__", Ar = Object.prototype, Or = Ar.hasOwnProperty;
function jr(t) {
  var e = this.__data__;
  if (W) {
    var n = e[t];
    return n === wr ? void 0 : n;
  }
  return Or.call(e, t) ? e[t] : void 0;
}
var Ir = Object.prototype, Sr = Ir.hasOwnProperty;
function Cr(t) {
  var e = this.__data__;
  return W ? e[t] !== void 0 : Sr.call(e, t);
}
var Mr = "__lodash_hash_undefined__";
function Er(t, e) {
  var n = this.__data__;
  return this.size += this.has(t) ? 0 : 1, n[t] = W && e === void 0 ? Mr : e, this;
}
function C(t) {
  var e = -1, n = t == null ? 0 : t.length;
  for (this.clear(); ++e < n; ) {
    var r = t[e];
    this.set(r[0], r[1]);
  }
}
C.prototype.clear = br;
C.prototype.delete = _r;
C.prototype.get = jr;
C.prototype.has = Cr;
C.prototype.set = Er;
function Tr() {
  this.__data__ = [], this.size = 0;
}
function et(t, e) {
  for (var n = t.length; n--; )
    if (tt(t[n][0], e))
      return n;
  return -1;
}
var $r = Array.prototype, zr = $r.splice;
function Fr(t) {
  var e = this.__data__, n = et(e, t);
  if (n < 0)
    return !1;
  var r = e.length - 1;
  return n == r ? e.pop() : zr.call(e, n, 1), --this.size, !0;
}
function Pr(t) {
  var e = this.__data__, n = et(e, t);
  return n < 0 ? void 0 : e[n][1];
}
function Vr(t) {
  return et(this.__data__, t) > -1;
}
function Nr(t, e) {
  var n = this.__data__, r = et(n, t);
  return r < 0 ? (++this.size, n.push([t, e])) : n[r][1] = e, this;
}
function w(t) {
  var e = -1, n = t == null ? 0 : t.length;
  for (this.clear(); ++e < n; ) {
    var r = t[e];
    this.set(r[0], r[1]);
  }
}
w.prototype.clear = Tr;
w.prototype.delete = Fr;
w.prototype.get = Pr;
w.prototype.has = Vr;
w.prototype.set = Nr;
var de = xt(z, "Map");
function Dr() {
  this.size = 0, this.__data__ = {
    hash: new C(),
    map: new (de || w)(),
    string: new C()
  };
}
function Rr(t) {
  var e = typeof t;
  return e == "string" || e == "number" || e == "symbol" || e == "boolean" ? t !== "__proto__" : t === null;
}
function nt(t, e) {
  var n = t.__data__;
  return Rr(e) ? n[typeof e == "string" ? "string" : "hash"] : n.map;
}
function Wr(t) {
  var e = nt(this, t).delete(t);
  return this.size -= e ? 1 : 0, e;
}
function Lr(t) {
  return nt(this, t).get(t);
}
function Ur(t) {
  return nt(this, t).has(t);
}
function Xr(t, e) {
  var n = nt(this, t), r = n.size;
  return n.set(t, e), this.size += n.size == r ? 0 : 1, this;
}
function F(t) {
  var e = -1, n = t == null ? 0 : t.length;
  for (this.clear(); ++e < n; ) {
    var r = t[e];
    this.set(r[0], r[1]);
  }
}
F.prototype.clear = Dr;
F.prototype.delete = Wr;
F.prototype.get = Lr;
F.prototype.has = Ur;
F.prototype.set = Xr;
var pe = yr(Object.getPrototypeOf, Object), Gr = "[object Object]", Hr = Function.prototype, Br = Object.prototype, he = Hr.toString, Yr = Br.hasOwnProperty, kr = he.call(Object);
function ye(t) {
  if (!H(t) || Q(t) != Gr)
    return !1;
  var e = pe(t);
  if (e === null)
    return !0;
  var n = Yr.call(e, "constructor") && e.constructor;
  return typeof n == "function" && n instanceof n && he.call(n) == kr;
}
function Kr() {
  this.__data__ = new w(), this.size = 0;
}
function Zr(t) {
  var e = this.__data__, n = e.delete(t);
  return this.size = e.size, n;
}
function qr(t) {
  return this.__data__.get(t);
}
function Jr(t) {
  return this.__data__.has(t);
}
var Qr = 200;
function to(t, e) {
  var n = this.__data__;
  if (n instanceof w) {
    var r = n.__data__;
    if (!de || r.length < Qr - 1)
      return r.push([t, e]), this.size = ++n.size, this;
    n = this.__data__ = new F(r);
  }
  return n.set(t, e), this.size = n.size, this;
}
function P(t) {
  var e = this.__data__ = new w(t);
  this.size = e.size;
}
P.prototype.clear = Kr;
P.prototype.delete = Zr;
P.prototype.get = qr;
P.prototype.has = Jr;
P.prototype.set = to;
var ge = typeof exports == "object" && exports && !exports.nodeType && exports, Dt = ge && typeof module == "object" && module && !module.nodeType && module, eo = Dt && Dt.exports === ge, Rt = eo ? z.Buffer : void 0;
Rt && Rt.allocUnsafe;
function no(t, e) {
  return t.slice();
}
var Wt = z.Uint8Array;
function ro(t) {
  var e = new t.constructor(t.byteLength);
  return new Wt(e).set(new Wt(t)), e;
}
function oo(t, e) {
  var n = ro(t.buffer);
  return new t.constructor(n, t.byteOffset, t.length);
}
function io(t) {
  return typeof t.constructor == "function" && !ie(t) ? pn(pe(t)) : {};
}
function ao(t) {
  return function(e, n, r) {
    for (var o = -1, i = Object(e), a = r(e), s = a.length; s--; ) {
      var c = a[++o];
      if (n(i[c], c, i) === !1)
        break;
    }
    return e;
  };
}
var so = ao();
function pt(t, e, n) {
  (n !== void 0 && !tt(t[e], n) || n === void 0 && !(e in t)) && bt(t, e, n);
}
function co(t) {
  return H(t) && _t(t);
}
function ht(t, e) {
  if (!(e === "constructor" && typeof t[e] == "function") && e != "__proto__")
    return t[e];
}
function uo(t) {
  return Cn(t, fe(t));
}
function lo(t, e, n, r, o, i, a) {
  var s = ht(t, n), c = ht(e, n), l = a.get(c);
  if (l) {
    pt(t, n, l);
    return;
  }
  var u = i ? i(s, c, n + "", t, e, a) : void 0, f = u === void 0;
  if (f) {
    var d = Y(c), p = !d && ce(c), y = !d && !p && le(c);
    u = c, d || p || y ? Y(s) ? u = s : co(s) ? u = yn(s) : p ? (f = !1, u = no(c)) : y ? (f = !1, u = oo(c)) : u = [] : ye(c) || dt(c) ? (u = s, dt(s) ? u = uo(s) : (!E(s) || vt(s)) && (u = io(c))) : f = !1;
  }
  f && (a.set(c, u), o(u, c, r, i, a), a.delete(c)), pt(t, n, u);
}
function wt(t, e, n, r, o) {
  t !== e && so(e, function(i, a) {
    if (o || (o = new P()), E(i))
      lo(t, e, a, n, wt, r, o);
    else {
      var s = r ? r(ht(t, a), i, a + "", t, e, o) : void 0;
      s === void 0 && (s = i), pt(t, a, s);
    }
  }, fe);
}
var fo = oe(function(t, e, n, r) {
  wt(t, e, n, r);
}), po = oe(function(t, e, n) {
  wt(t, e, n);
});
function K(t, e) {
  return e ? fo({}, t, e, (n, r) => {
    if (Y(n) && ye(r))
      return n.map((o) => po({}, o, r));
  }) : t;
}
function ho(t, e, n) {
  const { facetInfo: r } = e, o = t.value ? "value" : "map", i = t.rType;
  r.rowValues.forEach((a) => {
    r.columnValues.forEach((s) => {
      const c = n.getAxes({
        rowValue: a,
        columnValue: s
      }), l = new yt(
        t.data
      ).filterWithFacet({
        facetConfig: t.facet || {},
        rowValue: a,
        columnValue: s
      });
      o === "value" ? go(c, i, t, n) : o === "map" && yo(
        i,
        t,
        l,
        c,
        n
      );
    });
  });
}
function yo(t, e, n, r, o) {
  const i = t === "x" ? e.map.x1 : e.map.y1, a = t === "x" ? e.map.y1 : e.map.x1, s = n.getValues(i), c = n.getValues(a), l = r.fillXAxisConfig({
    config: X({
      xType: "value",
      xField: i,
      extendConfig: {
        ...gt,
        min: Math.min(...s),
        max: Math.max(...s)
      }
    }),
    xName: i
  }), u = r.fillYAxisConfig({
    config: G({
      yType: "value",
      yField: a,
      extendConfig: {
        ...mt,
        min: Math.min(...c),
        max: Math.max(...c)
      }
    }),
    yName: a
  }), f = K(
    {
      color: "black",
      type: "solid",
      width: 1
    },
    e.lineStyle
  ), d = mo(e, n, t), p = {
    type: "lines",
    xAxisId: l,
    yAxisId: u,
    coordinateSystem: "cartesian2d",
    polyline: !0,
    lineStyle: f,
    data: d
  };
  o.addSeries(p);
}
function go(t, e, n, r) {
  const o = t.getXAxisId(), i = t.getYAxisId(), a = e === "x" ? "xAxis" : "yAxis", s = n.value.value.map((u) => ({
    [a]: u
  })), c = K(
    {
      color: "black",
      type: "solid",
      width: 1
    },
    n.lineStyle
  ), l = {
    type: "line",
    xAxisId: o,
    yAxisId: i,
    data: [],
    markLine: {
      symbol: "none",
      label: { show: !1 },
      lineStyle: c,
      data: s,
      animation: !1
    }
  };
  r.addSeries(l);
}
function mo(t, e, n) {
  const r = e.dataset.source;
  if (n === "x") {
    const o = t.map.x1, i = t.map.y1, a = t.map.y2, s = t.data.dimensions.indexOf(o), c = t.data.dimensions.indexOf(i), l = t.data.dimensions.indexOf(a);
    return r.map((u) => {
      const f = u[s], d = u[c], p = u[l];
      return {
        coords: [
          [f, d],
          [f, p]
        ]
      };
    });
  }
  if (n === "y") {
    const o = t.map.y1, i = t.map.x1, a = t.map.x2, s = t.data.dimensions.indexOf(o), c = t.data.dimensions.indexOf(i), l = t.data.dimensions.indexOf(a);
    return r.map((u) => {
      const f = u[s], d = u[c], p = u[l];
      return {
        coords: [
          [d, f],
          [p, f]
        ]
      };
    });
  }
  throw new Error(`Invalid axisType ${n}`);
}
function vo(t, e, n) {
  switch (t.type) {
    case "bar":
      return Pe(
        t,
        e,
        n
      );
    case "line":
      return Ve(
        t,
        e,
        n
      );
    case "pie":
      return Ne(
        t,
        e,
        n
      );
    case "scatter":
      return De(
        t,
        e,
        n
      );
    case "effect-scatter":
      return Re(
        t,
        e,
        n
      );
    case "rule":
      return ho(
        t,
        e,
        n
      );
    default:
      throw new Error(`Unsupported mark type: ${t.type}`);
  }
}
const j = "-1", xo = {
  backgroundStyle: {
    borderWidth: 0
  },
  body: {
    itemStyle: {
      borderWidth: 0
    }
  }
};
class bo {
  constructor(e) {
    this.config = e, this.matrix = this.initMatrix(), this.axesManager = new _o(this.matrix), this.datasetManager = new Ao();
  }
  series = [];
  visualMap = [];
  datasetManager;
  axesManager;
  matrix;
  initMatrix() {
    const e = {
      ...xo,
      x: {
        data: [j],
        show: !1
      },
      y: {
        data: [j],
        show: !1
      }
    }, { rowValues: n, columnValues: r } = this.config.facetInfo || {};
    return n && (e.x.data = n), r && (e.y.data = r), e;
  }
  /**
   * getAxes
   */
  getAxes(e) {
    return this.axesManager.getAxes(e);
  }
  /**
   * addSeries
   */
  addSeries(e) {
    const n = `series-id-${this.series.length}`;
    return this.series.push({ ...e, id: n }), n;
  }
  /**
   * addVisualMap
   */
  addVisualMap(e) {
    this.visualMap.push(e);
  }
  toEChartsOption() {
    const { xAxis: e, yAxis: n, grid: r } = this.axesManager.toEChartsOption(), o = Oo(this.matrix), i = jo(
      r,
      o
    );
    return {
      xAxis: e,
      yAxis: n,
      grid: i,
      series: this.series,
      visualMap: this.visualMap,
      matrix: o,
      dataset: this.datasetManager.toDatasetOption()
    };
  }
}
class _o {
  itemMap;
  constructor(e) {
    this.itemMap = this.initItemMap(e);
  }
  initItemMap(e) {
    const n = /* @__PURE__ */ new Map();
    return e.x.data.forEach((r) => {
      e.y.data.forEach((o) => {
        const i = `${r}-${o}`, a = new wo({
          gridIdNumber: n.size,
          matrixCoord: [r, o]
        });
        n.set(i, a);
      });
    }), n;
  }
  getAxes(e) {
    const { rowValue: n, columnValue: r } = e, o = this.itemMap.get(`${n}-${r}`);
    if (!o)
      throw new Error("Invalid facet config");
    return o;
  }
  toEChartsOption() {
    const e = Array.from(this.itemMap.values()), n = e.flatMap((i) => i.xAxis), r = e.flatMap((i) => i.yAxis), o = e.flatMap((i) => i.grid);
    return {
      xAxis: n.length > 0 ? n : void 0,
      yAxis: r.length > 0 ? r : void 0,
      grid: o
    };
  }
}
class wo {
  xAxis = [];
  xAxisNamesIndexMap = /* @__PURE__ */ new Map();
  yAxis = [];
  yAxisNamesIndexMap = /* @__PURE__ */ new Map();
  grid = {};
  gridIdNumber;
  constructor(e) {
    const { gridIdNumber: n, matrixCoord: r } = e;
    this.gridIdNumber = n;
    const o = this.genGridId();
    this.grid = {
      id: o,
      coord: r,
      coordinateSystem: "matrix"
    };
  }
  genGridId() {
    return `gid-${this.gridIdNumber}`;
  }
  genXAxisId() {
    return `g-${this.gridIdNumber}-${this.xAxis.length}`;
  }
  genYAxisId() {
    return `g-${this.gridIdNumber}-${this.yAxis.length}`;
  }
  getXAxisId() {
    if (this.xAxis.length === 0) throw new Error("No xAxis");
    return `g-${this.gridIdNumber}-${this.xAxis.length - 1}`;
  }
  getYAxisId() {
    if (this.yAxis.length === 0) throw new Error("No yAxis");
    return `g-${this.gridIdNumber}-${this.yAxis.length - 1}`;
  }
  fillXAxisConfig(e) {
    if (this.xAxis.length > 2)
      throw new Error("Too many xAxis");
    const { config: n, xName: r } = e, o = this.xAxisNamesIndexMap.get(r);
    if (o !== void 0) {
      const a = this.xAxis[o];
      return Object.assign(a, {
        ...a,
        ...n
      }), a.id;
    }
    const i = this.genXAxisId();
    return this.xAxis.push({
      ...n,
      id: i,
      gridId: this.grid.id,
      show: !0
    }), this.xAxisNamesIndexMap.set(r, this.xAxis.length - 1), i;
  }
  fillYAxisConfig(e) {
    if (this.yAxis.length > 2)
      throw new Error("Too many yAxis");
    const { config: n, yName: r } = e, o = this.yAxisNamesIndexMap.get(r);
    if (o !== void 0) {
      const a = this.yAxis[o];
      return Object.assign(a, {
        ...a,
        ...n
      }), a.id;
    }
    const i = this.genYAxisId();
    return this.yAxis.push({
      ...n,
      id: i,
      gridId: this.grid.id,
      show: !0
    }), this.yAxisNamesIndexMap.set(r, this.yAxis.length - 1), i;
  }
}
class Ao {
  dataset = [];
  datasetMap = /* @__PURE__ */ new Map();
  datasetWithFilterSet = /* @__PURE__ */ new Set();
  /**
   * getDatasetId
   */
  getDatasetId(e) {
    const { data: n, filters: r } = e;
    let o = this.datasetMap.get(n);
    if (o || (o = this.genDataset(n)), r.length === 0)
      return o;
    const i = this.genWithFilterKey(o, r);
    return this.datasetWithFilterSet.has(i) || (this.datasetWithFilterSet.add(i), this.dataset.push({
      id: i,
      fromDatasetId: o,
      transform: {
        type: "filter",
        config: {
          and: r.map((a) => ({
            dimension: a.dim,
            [Lt(a.op)]: a.value
          }))
        }
      }
    })), i;
  }
  toDatasetOption() {
    return this.dataset;
  }
  genDataset(e) {
    const n = `ds${this.dataset.length}`;
    return this.datasetMap.set(e, n), this.dataset.push({
      id: n,
      dimensions: e.dimensions,
      source: e.source
    }), n;
  }
  genWithFilterKey(e, n) {
    const r = n.map((o) => `${o.dim}-${Lt(o.op)}-${o.value}`).join("-");
    return `${e}-${r}`;
  }
}
function Lt(t) {
  return t ?? "=";
}
function Oo(t) {
  const e = t.x.data[0] !== j, n = t.y.data[0] !== j;
  if (!(!e && !n))
    return {
      backgroundStyle: {
        borderWidth: 0
      },
      body: {
        itemStyle: {
          borderWidth: 0
        }
      },
      x: {
        ...t.x,
        show: t.x.data[0] !== j,
        levelSize: 30,
        itemStyle: {
          borderWidth: 0
        }
      },
      y: {
        ...t.y,
        show: t.y.data[0] !== j,
        levelSize: 30,
        itemStyle: {
          borderWidth: 0
        }
      }
    };
}
function jo(t, e) {
  if (e === void 0) {
    const { coord: n, coordinateSystem: r, ...o } = t[0];
    return [o];
  }
  return t;
}
function Io(t) {
  return t && typeof t == "object" && Object.keys(t).length === 0;
}
const So = {
  tooltip: {
    trigger: "axis"
  }
};
function Co(t) {
  const [e, n] = Mo(t);
  if (!n)
    return {};
  const { marks: r } = e, o = new bo(e);
  r.forEach(
    (a) => vo(a, e, o)
  );
  const i = K(
    o.toEChartsOption(),
    So
  );
  return K(i, t.echartsOptions);
}
function Mo(t) {
  const { data: e, facet: n, marks: r, echartsOptions: o } = t;
  let i = !0;
  const a = e && Ut(e), s = {
    data: null,
    row: null,
    column: null
  }, c = r.map((u) => {
    const f = u.data ?? a ?? { dimensions: [], source: [] };
    if (!f)
      throw new Error("Mark is missing data and no dataset is available");
    const d = Ut(f);
    d.source.length === 0 && (i = !1);
    const p = u.facet ?? n;
    if (s.row === null)
      s.row = p?.row;
    else if (p && s.row !== p.row)
      throw new Error("Facet row is not consistent");
    if (s.column === null)
      s.column = p?.column;
    else if (p && s.column !== p?.column)
      throw new Error("Facet column is not consistent");
    return s.data === null && (s.data = d), {
      ...u,
      data: d,
      facet: p
    };
  }), l = {
    rowValues: [j],
    columnValues: [j]
  };
  if (s.row || s.column) {
    const u = s.data;
    if (s.row) {
      const f = u.dimensions.indexOf(s.row);
      l.rowValues = Array.from(
        new Set(u.source.map((d) => d[f]))
      );
    }
    if (s.column) {
      const f = u.dimensions.indexOf(s.column);
      l.columnValues = Array.from(
        new Set(u.source.map((d) => d[f]))
      );
    }
  }
  return [{
    facetInfo: l,
    marks: c,
    echartsOptions: o
  }, i];
}
function Ut(t) {
  const e = typeof t == "function" ? t() : t;
  if (Array.isArray(e)) {
    if (e.length === 0)
      return { dimensions: [], source: [] };
    const n = Object.keys(e[0]), r = e.map((o) => Object.values(o));
    return { dimensions: n, source: r };
  } else if (Io(e))
    return { dimensions: [], source: [] };
  return e;
}
var Eo = typeof global == "object" && global && global.Object === Object && global, To = typeof self == "object" && self && self.Object === Object && self, At = Eo || To || Function("return this")(), $ = At.Symbol, me = Object.prototype, $o = me.hasOwnProperty, zo = me.toString, D = $ ? $.toStringTag : void 0;
function Fo(t) {
  var e = $o.call(t, D), n = t[D];
  try {
    t[D] = void 0;
    var r = !0;
  } catch {
  }
  var o = zo.call(t);
  return r && (e ? t[D] = n : delete t[D]), o;
}
var Po = Object.prototype, Vo = Po.toString;
function No(t) {
  return Vo.call(t);
}
var Do = "[object Null]", Ro = "[object Undefined]", Xt = $ ? $.toStringTag : void 0;
function ve(t) {
  return t == null ? t === void 0 ? Ro : Do : Xt && Xt in Object(t) ? Fo(t) : No(t);
}
function Wo(t) {
  return t != null && typeof t == "object";
}
var Lo = "[object Symbol]";
function Ot(t) {
  return typeof t == "symbol" || Wo(t) && ve(t) == Lo;
}
function Uo(t, e) {
  for (var n = -1, r = t == null ? 0 : t.length, o = Array(r); ++n < r; )
    o[n] = e(t[n], n, t);
  return o;
}
var jt = Array.isArray, Gt = $ ? $.prototype : void 0, Ht = Gt ? Gt.toString : void 0;
function xe(t) {
  if (typeof t == "string")
    return t;
  if (jt(t))
    return Uo(t, xe) + "";
  if (Ot(t))
    return Ht ? Ht.call(t) : "";
  var e = t + "";
  return e == "0" && 1 / t == -1 / 0 ? "-0" : e;
}
function Z(t) {
  var e = typeof t;
  return t != null && (e == "object" || e == "function");
}
var Xo = "[object AsyncFunction]", Go = "[object Function]", Ho = "[object GeneratorFunction]", Bo = "[object Proxy]";
function Yo(t) {
  if (!Z(t))
    return !1;
  var e = ve(t);
  return e == Go || e == Ho || e == Xo || e == Bo;
}
var ft = At["__core-js_shared__"], Bt = function() {
  var t = /[^.]+$/.exec(ft && ft.keys && ft.keys.IE_PROTO || "");
  return t ? "Symbol(src)_1." + t : "";
}();
function ko(t) {
  return !!Bt && Bt in t;
}
var Ko = Function.prototype, Zo = Ko.toString;
function qo(t) {
  if (t != null) {
    try {
      return Zo.call(t);
    } catch {
    }
    try {
      return t + "";
    } catch {
    }
  }
  return "";
}
var Jo = /[\\^$.*+?()[\]{}|]/g, Qo = /^\[object .+?Constructor\]$/, ti = Function.prototype, ei = Object.prototype, ni = ti.toString, ri = ei.hasOwnProperty, oi = RegExp(
  "^" + ni.call(ri).replace(Jo, "\\$&").replace(/hasOwnProperty|(function).*?(?=\\\()| for .+?(?=\\\])/g, "$1.*?") + "$"
);
function ii(t) {
  if (!Z(t) || ko(t))
    return !1;
  var e = Yo(t) ? oi : Qo;
  return e.test(qo(t));
}
function ai(t, e) {
  return t?.[e];
}
function It(t, e) {
  var n = ai(t, e);
  return ii(n) ? n : void 0;
}
var Yt = function() {
  try {
    var t = It(Object, "defineProperty");
    return t({}, "", {}), t;
  } catch {
  }
}(), si = 9007199254740991, ci = /^(?:0|[1-9]\d*)$/;
function ui(t, e) {
  var n = typeof t;
  return e = e ?? si, !!e && (n == "number" || n != "symbol" && ci.test(t)) && t > -1 && t % 1 == 0 && t < e;
}
function li(t, e, n) {
  e == "__proto__" && Yt ? Yt(t, e, {
    configurable: !0,
    enumerable: !0,
    value: n,
    writable: !0
  }) : t[e] = n;
}
function be(t, e) {
  return t === e || t !== t && e !== e;
}
var fi = Object.prototype, di = fi.hasOwnProperty;
function pi(t, e, n) {
  var r = t[e];
  (!(di.call(t, e) && be(r, n)) || n === void 0 && !(e in t)) && li(t, e, n);
}
var hi = /\.|\[(?:[^[\]]*|(["'])(?:(?!\1)[^\\]|\\.)*?\1)\]/, yi = /^\w*$/;
function gi(t, e) {
  if (jt(t))
    return !1;
  var n = typeof t;
  return n == "number" || n == "symbol" || n == "boolean" || t == null || Ot(t) ? !0 : yi.test(t) || !hi.test(t) || e != null && t in Object(e);
}
var L = It(Object, "create");
function mi() {
  this.__data__ = L ? L(null) : {}, this.size = 0;
}
function vi(t) {
  var e = this.has(t) && delete this.__data__[t];
  return this.size -= e ? 1 : 0, e;
}
var xi = "__lodash_hash_undefined__", bi = Object.prototype, _i = bi.hasOwnProperty;
function wi(t) {
  var e = this.__data__;
  if (L) {
    var n = e[t];
    return n === xi ? void 0 : n;
  }
  return _i.call(e, t) ? e[t] : void 0;
}
var Ai = Object.prototype, Oi = Ai.hasOwnProperty;
function ji(t) {
  var e = this.__data__;
  return L ? e[t] !== void 0 : Oi.call(e, t);
}
var Ii = "__lodash_hash_undefined__";
function Si(t, e) {
  var n = this.__data__;
  return this.size += this.has(t) ? 0 : 1, n[t] = L && e === void 0 ? Ii : e, this;
}
function M(t) {
  var e = -1, n = t == null ? 0 : t.length;
  for (this.clear(); ++e < n; ) {
    var r = t[e];
    this.set(r[0], r[1]);
  }
}
M.prototype.clear = mi;
M.prototype.delete = vi;
M.prototype.get = wi;
M.prototype.has = ji;
M.prototype.set = Si;
function Ci() {
  this.__data__ = [], this.size = 0;
}
function rt(t, e) {
  for (var n = t.length; n--; )
    if (be(t[n][0], e))
      return n;
  return -1;
}
var Mi = Array.prototype, Ei = Mi.splice;
function Ti(t) {
  var e = this.__data__, n = rt(e, t);
  if (n < 0)
    return !1;
  var r = e.length - 1;
  return n == r ? e.pop() : Ei.call(e, n, 1), --this.size, !0;
}
function $i(t) {
  var e = this.__data__, n = rt(e, t);
  return n < 0 ? void 0 : e[n][1];
}
function zi(t) {
  return rt(this.__data__, t) > -1;
}
function Fi(t, e) {
  var n = this.__data__, r = rt(n, t);
  return r < 0 ? (++this.size, n.push([t, e])) : n[r][1] = e, this;
}
function V(t) {
  var e = -1, n = t == null ? 0 : t.length;
  for (this.clear(); ++e < n; ) {
    var r = t[e];
    this.set(r[0], r[1]);
  }
}
V.prototype.clear = Ci;
V.prototype.delete = Ti;
V.prototype.get = $i;
V.prototype.has = zi;
V.prototype.set = Fi;
var Pi = It(At, "Map");
function Vi() {
  this.size = 0, this.__data__ = {
    hash: new M(),
    map: new (Pi || V)(),
    string: new M()
  };
}
function Ni(t) {
  var e = typeof t;
  return e == "string" || e == "number" || e == "symbol" || e == "boolean" ? t !== "__proto__" : t === null;
}
function ot(t, e) {
  var n = t.__data__;
  return Ni(e) ? n[typeof e == "string" ? "string" : "hash"] : n.map;
}
function Di(t) {
  var e = ot(this, t).delete(t);
  return this.size -= e ? 1 : 0, e;
}
function Ri(t) {
  return ot(this, t).get(t);
}
function Wi(t) {
  return ot(this, t).has(t);
}
function Li(t, e) {
  var n = ot(this, t), r = n.size;
  return n.set(t, e), this.size += n.size == r ? 0 : 1, this;
}
function T(t) {
  var e = -1, n = t == null ? 0 : t.length;
  for (this.clear(); ++e < n; ) {
    var r = t[e];
    this.set(r[0], r[1]);
  }
}
T.prototype.clear = Vi;
T.prototype.delete = Di;
T.prototype.get = Ri;
T.prototype.has = Wi;
T.prototype.set = Li;
var Ui = "Expected a function";
function St(t, e) {
  if (typeof t != "function" || e != null && typeof e != "function")
    throw new TypeError(Ui);
  var n = function() {
    var r = arguments, o = e ? e.apply(this, r) : r[0], i = n.cache;
    if (i.has(o))
      return i.get(o);
    var a = t.apply(this, r);
    return n.cache = i.set(o, a) || i, a;
  };
  return n.cache = new (St.Cache || T)(), n;
}
St.Cache = T;
var Xi = 500;
function Gi(t) {
  var e = St(t, function(r) {
    return n.size === Xi && n.clear(), r;
  }), n = e.cache;
  return e;
}
var Hi = /[^.[\]]+|\[(?:(-?\d+(?:\.\d+)?)|(["'])((?:(?!\2)[^\\]|\\.)*?)\2)\]|(?=(?:\.|\[\])(?:\.|\[\]|$))/g, Bi = /\\(\\)?/g, Yi = Gi(function(t) {
  var e = [];
  return t.charCodeAt(0) === 46 && e.push(""), t.replace(Hi, function(n, r, o, i) {
    e.push(o ? i.replace(Bi, "$1") : r || n);
  }), e;
});
function ki(t) {
  return t == null ? "" : xe(t);
}
function Ki(t, e) {
  return jt(t) ? t : gi(t, e) ? [t] : Yi(ki(t));
}
function Zi(t) {
  if (typeof t == "string" || Ot(t))
    return t;
  var e = t + "";
  return e == "0" && 1 / t == -1 / 0 ? "-0" : e;
}
function qi(t, e, n, r) {
  if (!Z(t))
    return t;
  e = Ki(e, t);
  for (var o = -1, i = e.length, a = i - 1, s = t; s != null && ++o < i; ) {
    var c = Zi(e[o]), l = n;
    if (c === "__proto__" || c === "constructor" || c === "prototype")
      return t;
    if (o != a) {
      var u = s[c];
      l = void 0, l === void 0 && (l = Z(u) ? u : ui(e[o + 1]) ? [] : {});
    }
    pi(s, c, l), s = s[c];
  }
  return t;
}
function Ji(t, e, n) {
  return t == null ? t : qi(t, e, n);
}
function kt(t, e) {
  return qt.init(t, e.theme, e.initOptions);
}
function Qi(t, e, n) {
  Zt(
    () => n.resizeOption,
    (r, o, i) => {
      let a = null;
      if (r) {
        const { offsetWidth: s, offsetHeight: c } = t, { throttle: l = 100 } = r;
        let u = !1;
        const f = () => {
          e.resize();
        }, d = l ? qt.throttle(f, l) : f;
        a = new ResizeObserver(() => {
          !u && (u = !0, t.offsetWidth === s && t.offsetHeight === c) || d();
        }), a.observe(t);
      }
      i(() => {
        a && (a.disconnect(), a = null);
      });
    },
    { deep: !0, immediate: !0 }
  );
}
function Kt(t, e, n) {
  t.setOption(n || {}, e.updateOptions || {});
}
function ta(t, e, n) {
  const { chartEvents: r, zrEvents: o } = n;
  r && r.forEach((i) => {
    t.on(i, (...a) => {
      if (a.length > 0) {
        const s = a[0];
        delete s.event, delete s.$vars;
      }
      e(`chart:${i}`, ...a);
    });
  }), o && o.forEach((i) => {
    t.getZr().on(i, (...a) => e(`zr:${i}`, ...a));
  });
}
function ea(t) {
  const { getRef: e } = Te(), n = (t.refSets || []).map((r) => {
    const { path: o, ref: i } = r;
    return {
      path: o,
      ref: e(i)
    };
  });
  return _e(() => {
    if (t.optionType === "dict")
      return t.option;
    const r = t.option;
    return n.forEach((i) => {
      const { path: a, ref: s } = i;
      Ji(r, a, s.value);
    }), Co(r);
  });
}
const oa = /* @__PURE__ */ we({
  __name: "echarts",
  props: {
    option: {},
    refSets: {},
    optionType: {},
    theme: {},
    initOptions: {},
    resizeOption: {},
    updateOptions: {},
    chartEvents: {},
    zrEvents: {}
  },
  setup(t, { emit: e }) {
    const n = t, r = Ae("root"), o = Oe(), i = e, a = ea(n);
    je(() => {
      r.value && (o.value = kt(r.value, n), Qi(r.value, o.value, n), Kt(o.value, n, a.value), ta(o.value, i, n));
    }), Zt(
      a,
      (c) => {
        !o.value && r.value && (o.value = kt(r.value, n)), Kt(o.value, n, c);
      },
      { deep: !0 }
    );
    const s = Ie();
    return (c, l) => (Ce(), Se("div", Me({ ref: "root" }, Ee(s)), null, 16));
  }
});
export {
  oa as default
};
