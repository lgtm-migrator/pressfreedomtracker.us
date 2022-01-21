import React, { useRef } from 'react'
import { ParentSize } from '@visx/responsive'
import { TreeMap } from './TreeMap.js'
import { USMap } from './USMap.js'
import { BarChartHomepage } from './BarChartHomepage.js'
import { HomepageSelection } from './HomepageSelection.js'
import {
  filterDatasetByFiltersApplied,
  groupByMonthSorted,
  monthIndexes,
  groupByGeo,
  countIncidentsOutsideUS,
  categoriesColors,
} from '../lib/utilities.js'

const categoriesSlugs = {
  'Arrest/Criminal Charge': 'arrest-criminal-charge',
  'Border Stop': 'border-stop',
  'Subpoena/Legal Order': 'subpoena',
  'Leak Case': 'leak-case',
  'Equipment Search or Seizure': 'equipment-search-seizure-or-damage',
  'Physical Attack': 'physical-attack',
  'Denial of Access': 'denial-access',
  'Chilling Statement': 'chilling-statement',
  'Other Incident': 'other-incident',
  'Prior Restraint': 'prior-restraint',
  'Equipment Damage': 'equipment-damage',
}

function goToFilterPage(filtersApplied, currentDate) {
  const baseURL =
    filtersApplied.category === undefined
      ? `https://pressfreedomtracker.us/all-incidents/?`
      : `https://pressfreedomtracker.us/${categoriesSlugs[filtersApplied.category]}/?`

  const parameters = []

  if (filtersApplied.monthName !== undefined) {
    const monthNumber = monthIndexes[filtersApplied.monthName]
    const year = !filtersApplied.sixMonths
      ? filtersApplied.year
      : currentDate.getMonth() > 6 || monthNumber <= 6
      ? currentDate.getFullYear()
      : currentDate.getFullYear() - 1
    const firstDayMonth = `${year}-${monthNumber}-1`
    const lastDayMonth = `${year}-${monthNumber}-${new Date(year, monthNumber, 0).getDate()}`
    parameters.push(`date_lower=${firstDayMonth}&date_upper=${lastDayMonth}`)
  }

  if (filtersApplied.city !== undefined) {
    parameters.push(`city=${filtersApplied.city.replace(' ', '%20')}`)
  }

  if (filtersApplied.year !== null && filtersApplied.monthName === undefined) {
    parameters.push(`date_lower=${filtersApplied.year}-1-1&date_upper=${filtersApplied.year}-12-31`)
  }

  if (filtersApplied.sixMonths && filtersApplied.monthName === undefined) {
    const currentMonth = currentDate.getMonth()
    const currentYear = currentDate.getFullYear()
    const previousYear = currentDate.getFullYear() - 1
    const firstDate = `${currentMonth > 5 ? currentYear : previousYear}-${
      currentMonth > 5 ? currentMonth - 5 : 11 - (5 - currentMonth)
    }-1`
    const lastDate = `${currentYear}-${currentMonth}-${new Date(
      currentYear,
      currentMonth,
      0
    ).getDay()}`
    parameters.push(`date_lower=${firstDate}&date_upper=${lastDate}`)
  }

  if (filtersApplied.tag !== null) {
    parameters.push(`tags=${filtersApplied.tag.replace(' ', '-')}`)
  }

  const url = `${baseURL}${parameters.join('&')}`
  window.alert(`Going to page ${url}`)
}

export function HomepageMainCharts(props) {
  return (
    <ParentSize>
      {(parent) => <HomepageMainChartsWidth {...props} width={parent.width} />}
    </ParentSize>
  )
}

export function HomepageMainChartsWidth({ data: dataset, width, currentDate = new Date() }) {
  const [filtersApplied, setFiltersApplied] = React.useState({
    tag: null,
    year: null,
    sixMonths: true,
  })
  const treemapWrapper = useRef()
  const usmapWrapper = useRef()
  const barchartWrapper = useRef()

  const chartWidth = width > 970 ? width / 3 : width
  const chartHeight = width > 970 ? 500 : 480

  const datasetFiltered = filterDatasetByFiltersApplied(dataset, filtersApplied, currentDate)

  const datasetAggregatedByGeo = groupByGeo(datasetFiltered)
  const incidentsOutsideUS = countIncidentsOutsideUS(datasetFiltered)

  const datasetGroupedByMonth = groupByMonthSorted(
    datasetFiltered,
    filtersApplied.sixMonths,
    currentDate
  )

  return (
    <>
      <HomepageSelection
        width={width}
        height={'40px'}
        data={dataset}
        numberOfTags={5}
        filtersApplied={filtersApplied}
        setFiltersApplied={setFiltersApplied}
      />
      <div className={'hpChartContainer'} style={{ width: width }}>
        <div className={'hpChart'} ref={treemapWrapper}>
          <TreeMap
            data={datasetFiltered}
            width={chartWidth}
            height={chartHeight}
            isHomePageDesktopView={width > 970}
            minimumBarHeight={35}
            categoryColumn={'categories'}
            titleLabel={'incidents'}
            openSearchPage={(category) => {
              goToFilterPage({ ...filtersApplied, category }, currentDate)
            }}
            wrapper={treemapWrapper}
            categoriesColors={(d) => categoriesColors[d]}
            allCategories={Object.keys(categoriesColors)}
          />
        </div>
        <div className={'hpChart'} ref={usmapWrapper}>
          <USMap
            data={datasetAggregatedByGeo}
            incidentsOutsideUS={incidentsOutsideUS}
            width={chartWidth}
            height={chartHeight}
            openSearchPage={(city) => {
              goToFilterPage({ ...filtersApplied, city }, currentDate)
            }}
            wrapper={usmapWrapper}
          />
        </div>
        <div className={'hpChart'} ref={barchartWrapper}>
          <BarChartHomepage
            data={datasetGroupedByMonth}
            x={'monthName'}
            y={'numberOfIncidents'}
            titleLabel={'incidents'}
            width={chartWidth}
            height={chartHeight}
            isMobileView={width < 970}
            openSearchPage={(monthName) => {
              goToFilterPage({ ...filtersApplied, monthName }, currentDate)
            }}
            wrapper={barchartWrapper}
          />
        </div>
      </div>
    </>
  )
}
