import * as d3 from 'd3'
import { uniq } from 'lodash'
import usStates from '../data/us-states-coordinates.json'

export const monthNames = [
	'Jan',
	'Feb',
	'Mar',
	'Apr',
	'May',
	'Jun',
	'Jul',
	'Aug',
	'Sep',
	'Oct',
	'Nov',
	'Dec',
]

export const monthIndexes = {
	Jan: 1,
	Feb: 2,
	Mar: 3,
	Apr: 4,
	May: 5,
	Jun: 6,
	Jul: 7,
	Aug: 8,
	Sep: 9,
	Oct: 10,
	Nov: 11,
	Dec: 12,
}

export const categoriesSlugs = {
	'Arrest/Criminal Charge': 'arrest-criminal-charge',
	'Border Stop': 'border-stop',
	'Subpoena/Legal Order': 'subpoena',
	'Leak Case': 'leak-case',
	'Equipment Search or Seizure': 'equipment-search-seizure-or-damage',
	'Assault': 'assault',
	'Denial of Access': 'denial-access',
	'Chilling Statement': 'chilling-statement',
	'Other Incident': 'other-incident',
	'Prior Restraint': 'prior-restraint',
	'Equipment Damage': 'equipment-damage',
}

export function getFilteredUrl(databasePath, filtersApplied, currentDate) {
	const origin = window.location.origin
	const baseUrl = filtersApplied.category === undefined || categoriesSlugs[filtersApplied.category] === undefined
		? `${origin}${databasePath}?`
		: `${origin}/${categoriesSlugs[filtersApplied.category]}/?`

	const parameters = []

	if (!!parseInt(filtersApplied.category)) {
		parameters.push(`categories=${filtersApplied.category}`)
	}

	if (filtersApplied.monthName !== undefined) {
		const monthNumber = monthIndexes[filtersApplied.monthName]
		const year = !filtersApplied.sixMonths
			? filtersApplied.year
			: currentDate.getUTCMonth() > 6 || monthNumber <= 6
			? currentDate.getUTCFullYear()
			: currentDate.getUTCFullYear() - 1
		const paddedMonthNumber = String(monthNumber).padStart(2, '0')
		const firstDayMonth = `${year}-${paddedMonthNumber}-01`
		const lastDayMonth = `${year}-${paddedMonthNumber}-${new Date(year, monthNumber, 0).getDate()}`
		parameters.push(`date_lower=${firstDayMonth}&date_upper=${lastDayMonth}`)
	}

	if (filtersApplied.state !== undefined) {
		parameters.push(`state=${filtersApplied.state.replace(' ', '+')}`)
	}

	if (filtersApplied.year !== null && filtersApplied.monthName === undefined) {
		parameters.push(`date_lower=${filtersApplied.year}-01-01&date_upper=${filtersApplied.year}-12-31`)
	}

	if (filtersApplied.sixMonths && filtersApplied.monthName === undefined) {
		const currentMonth = currentDate.getUTCMonth()
		const currentYear = currentDate.getUTCFullYear()

		const lastDate = new Date(currentYear, currentMonth + 1, 0)  // last day of the current month
		const firstDate = new Date(currentYear, currentMonth - 5, 1)  // first day of the month five months ago
		const firstDateFormatted = firstDate.toISOString().substring(0, 10)  // Extract the date portion of the ISO datetime
		const lastDateFormatted = lastDate.toISOString().substring(0, 10)

		parameters.push(`date_lower=${firstDateFormatted}&date_upper=${lastDateFormatted}`)
	}

	if (filtersApplied.tag !== undefined && filtersApplied.tag !== null) {
		parameters.push(`tags=${filtersApplied.tag.replace(' ', '+')}`)
	}

	return `${baseUrl}${parameters.join('&')}`
}

export function goToFilterPage(databasePath, filtersApplied, currentDate) {
	const url = getFilteredUrl(databasePath, filtersApplied, currentDate)
	window.location = url
}

export function filterDatasetByTag(dataset, tag) {
	return dataset.filter(
		(d) =>
			d.tags &&
			d.tags
				.split(',')
				.map((s) => s.trim())
				.includes(tag)
	)
}

export function filterDatasetByYear(dataset, year) {
	return dataset.filter((d) => d.date.getUTCFullYear() === year)
}

// Filter to the last six months, inclusive on the *currentDate* end
export function filterDatasetByLastSixMonths(dataset, currentDate) {
	const sixMonthsAgo = d3.utcMonth.offset(currentDate, -6)
	return dataset.filter(d => +d.date > +sixMonthsAgo && +d.date <= +currentDate)
}

export function filterDatasetByFiltersApplied(originalDataset, filtersApplied, currentDate) {
	const datasetFilteredByTag =
		filtersApplied.tag !== null
			? filterDatasetByTag(originalDataset, filtersApplied.tag)
			: originalDataset
	const datasetFilteredByYear =
		filtersApplied.year !== null
			? filterDatasetByYear(datasetFilteredByTag, filtersApplied.year)
			: datasetFilteredByTag
	const datasetFilteredBySixMonths =
		filtersApplied.sixMonths !== false
			? filterDatasetByLastSixMonths(datasetFilteredByYear, currentDate)
			: datasetFilteredByYear

	return datasetFilteredBySixMonths
}

export function groupByMonthSorted(dataset, isLastSixMonths, currentDate) {
	const datasetGroupedByMonth = d3
		.groups(
			dataset.map((d) => ({ month: d.date.getUTCMonth() })),
			(d) => d.month
		)
		.map((d) => ({ month: d[0], monthName: monthNames[d[0]], numberOfIncidents: d[1].length }))

	const currentMonth = currentDate.getUTCMonth()
	const monthsConsidered =
		currentMonth < 5
			? monthNames.slice(currentMonth - 5).concat(monthNames.slice(0, currentMonth + 1))
			: monthNames.slice(currentMonth - 5, currentMonth + 1)

	// If yearly selection, we sort the array by month
	// If last six months selection, we sort the array based on the last six months
	const datasetGroupedByMonthSorted = isLastSixMonths
		? monthsConsidered
				.map((d) =>
					datasetGroupedByMonth.filter((e) => e.monthName === d).length === 0
						? { month: monthIndexes[d] - 1, monthName: d, numberOfIncidents: 0 }
						: datasetGroupedByMonth.filter((e) => e.monthName === d)
				)
				.flat()
		: monthNames
				.map((d) =>
					datasetGroupedByMonth.filter((e) => e.monthName === d).length === 0
						? { month: monthIndexes[d] - 1, monthName: d, numberOfIncidents: 0 }
						: datasetGroupedByMonth.filter((e) => e.monthName === d)
				)
				.flat()

	return datasetGroupedByMonthSorted
}

export function groupByYearsSorted(dataset) {
	const datasetGroupedByYear = d3
		.groups(
			dataset.map((d) => ({ year: d.date.getUTCFullYear() })),
			(d) => d.year
		)
		.map((d) => ({ year: d[0], numberOfIncidents: d[1].length }))

	const datasetGroupedByYearSorted = datasetGroupedByYear.sort((a, b) => a.year - b.year)
	return datasetGroupedByYearSorted
}

export function groupByCity(dataset) {
	// Pick cities from dataset with coordinates
	const cities = dataset.map((d) => ({
		latitude: d.latitude,
		longitude: d.longitude,
		city: d.city,
		state: d.state !== undefined ? d.state : 'Abroad',
	}))

	// Group dataset by city and coordinates (some cities have the same name)
	// Reorganize the array as: [{latitude: .., longitude: .., name: .., numberOfIncidents: ..}, {..}, ...]
	// Sort the array to plot first the cities with the higher number of incidents
	const incidentsGroupedByCity = d3
		.flatRollup(
			cities,
			(v) => v.length,
			(d) => d.city,
			(d) => d.state,
			(d) => d.latitude,
			(d) => d.longitude
		)
		.map(([city, state, latitude, longitude, numberOfIncidents]) => ({
			city,
			state,
			latitude,
			longitude,
			numberOfIncidents,
		}))
		.sort((a, b) => b.numberOfIncidents - a.numberOfIncidents)

	// Remove rows without coordinates
	const incidentsGroupedFiltered = incidentsGroupedByCity.filter(
		(d) => d.latitude !== 'None' && d.longitude !== 'None'
	)

	if (incidentsGroupedByCity.length !== incidentsGroupedFiltered.length) {
		const citiesMissing = incidentsGroupedByCity - incidentsGroupedFiltered
		console.debug(`There are ${citiesMissing} cities without coordinates`)
	}

	return incidentsGroupedFiltered
}

export function groupByState(dataset) {
	const usStatesList = usStates.map((d) => d.acronym)

	// Pick cities from dataset with coordinates
	const states = dataset.map((d) => ({
		acronym: d.state !== undefined && usStatesList.includes(d.state) ? d.state : 'Abroad',
	}))

	// Group dataset by state
	// Sort the array to plot first the cities with the higher number of incidents
	const incidentsGroupedByState = d3
		.flatRollup(
			states,
			(v) => v.length,
			(d) => d.acronym
		)
		.map(([acronym, numberOfIncidents]) => ({
			state: acronym !== 'Abroad' ? usStates.find((d) => d.acronym === acronym).state : 'Abroad',
			usCode: acronym !== 'Abroad' ? acronym : null,
			numberOfIncidents,
			latitude:
				acronym !== 'Abroad' ? usStates.find((d) => d.acronym === acronym).latitude : undefined,
			longitude:
				acronym !== 'Abroad' ? usStates.find((d) => d.acronym === acronym).longitude : undefined,
		}))
		.sort((a, b) => b.numberOfIncidents - a.numberOfIncidents)

	return incidentsGroupedByState
}

export function countIncidentsOutsideUS(dataset) {
	const usStatesList = usStates.map((d) => d.acronym)
	// Added a quick hack to exclude Puerto Rico from the outside the US list
	// We should handle this more elegantly in the future
	return dataset.filter((d) => d.state === undefined || (!usStatesList.includes(d.state) && d.state !== 'PR')).length
}

export const categoriesColors = {
	'Arrest/Criminal Charge': '#669599',
	'Assault': '#E07A5F',
	'Border Stop': '#FBE0BC',
	'Chilling Statement': '#F4C280',
	'Denial of Access': '#7EBBC8',
	'Equipment Damage': '#B0829D',
	'Equipment Search or Seizure': '#63729A',
	'Leak Case': '#F9B29F',
	'Prior Restraint': '#98C9CD',
	'Subpoena/Legal Order': '#E2B6D0',
	'Other Incident': '#B2B8E5',
}

// barChart Filter functions
export function firstDayOfMonth(date) {
	return d3.timeMonth.floor(new Date(date))
}

export function firstDayOfNextMonth(date) {
	return d3.timeMonth.ceil(new Date(date))
}

export function isSubset(subset, container) {
	// all elements of subset must be present in container
	return subset.every((element) => container.includes(element))
}

export const colors = [
	'#E07A5F',
	'#669599',
	'#B0829D',
	'#63729A',
	'#F4C280',
	'#7EBBC8',
	'#F9B29F',
	'#98C9CD',
	'#E2B6D0',
	'#B2B8E5',
	'#FBE0BC',
	'#BAECF7',
	'#975544',
	'#435556',
	'#6B5261',
	'#484B6B',
	'#957932',
	'#54767D',
]
export function removeElement(array, element) {
	return array.filter((d) => d !== element)
}

export function formatDataset(dataset) {
	return dataset
		.map((d) => ({
			...d,
			categories: uniq(d.categories?.split(',').map((c) => c.trim())) || [],
		}))
		.map((d) => ({
			...d,
			tags: uniq(d.tags?.split(',').map((c) => c.trim())) || [],
		}))
}

export function isDateValid(date) {
	return !Number.isNaN(new Date(date).getYear())
}


// Return a range of numbers, including both start and stop terms.
// rangeInclusive(0, 4, 1)  --> [0, 1, 2, 3, 4]
export function rangeInclusive(start, stop, step) {
	return Array.from({ length: (stop - start) / step + 1}, (_, i) => start + (i * step));
}
