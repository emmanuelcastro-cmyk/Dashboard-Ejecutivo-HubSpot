# Quartux Dashboard - Per-Panel Date Filtering

## Phase 1: Global Date Filter State & Filter Bar Component ✅
- [x] Add global date filter state vars to DashboardState (date_preset, custom_start, custom_end, date_field)
- [x] Add computed var filtered_deals_by_date that applies date range on top of pipeline/owner filters
- [x] Build reusable date_filter_bar() component with preset chips + custom date inputs
- [x] Integrate filter bar into Resumen, Pipeline, Equipo, Actividad, Tiempo pages
- [x] Update all existing computed vars to use date-filtered deals

## Phase 2: Update All Pages to Use Date-Filtered Data
- [ ] Update Resumen KPIs, breakdowns, and gauges to use date-filtered deals
- [ ] Update Pipeline charts, funnels, scatter, and status distribution
- [ ] Update Equipo table, rankings, radar chart, and advisor modal
- [ ] Update Actividad weekly charts, stage movements, heatmap, and comparison table
- [ ] Update Tiempo time series charts and scatter plot

## Phase 3: Scorecard, Metas & Polish
- [ ] Update Scorecard to respect global date filters where applicable
- [ ] Update Metas gauges and forecast to reflect filtered data
- [ ] Ensure Monitor page shows filter context
- [ ] Final visual consistency and edge case handling
