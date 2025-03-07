import React from 'react'
import PropTypes from 'prop-types'


function isDateValid(date) {
	return !Number.isNaN(new Date(date).getYear())
}


function DateFilter({
	name,
	label,
	value,
	setFilterParameters,
}) {
	let lowerId = `id_${name}_after`
	let upperId = `id_${name}_before`
	let lowerValue = value.min?.toISOString()?.split('T')[0]
	let upperValue = value.max?.toISOString()?.split('T')[0]
	return (
		<>
			<div className={"filters__field-row"}>
				<div className="filters__field-label">
					<label htmlFor={lowerId}>{label} after</label>
				</div>
				<input
					type="date"
					value={lowerValue ?? ""}
					name={name}
					id={lowerId}
					onChange={(event) => {
						let newMinDate = event.target.value
						newMinDate = isDateValid(newMinDate) ? new Date(newMinDate) : null
						const newDateRange = (oldDateRange) => {
							return { ...oldDateRange, min: newMinDate }
						}
						setFilterParameters(name, newDateRange)
					}}
				/>
			</div>
			<div className={"filters__field-row"}>
				<div className="filters__field-label">
					<label htmlFor={upperId}>{label} before</label>
				</div>
				<input
					type="date"
					name={name}
					value={upperValue ?? ""}
					id={upperId}
					onChange={(event) => {
						let newMaxDate = event.target.value
						newMaxDate = isDateValid(newMaxDate) ? new Date(newMaxDate) : null
						const newDateRange = (oldDateRange) => {
							return { ...oldDateRange, max: newMaxDate }
						}
						setFilterParameters(name, newDateRange)
					}}
				/>
			</div>
		</>
	)
}

function TextFilter({
	name,
	label,
	value,
	handleFilterChange,
}) {
	let id = `id_${name}`
	return (
		<div className={"filters__field-row"}>
			<div className={"filters__field-label"}>
				<label htmlFor={id}>{label}</label>
			</div>

			<input
				value={value}
				type="text"
				name={name}
				className="text-field--single"
				autoComplete="off"
				onChange={handleFilterChange}
				id={id}
			/>
		</div>
	)
}

TextFilter.propTypes = {
	name: PropTypes.string.isRequired,
	label: PropTypes.string.isRequired,
	value: PropTypes.string,
	handleFilterChange: PropTypes.func.isRequired,
}

function SelectFilter({
	name,
	label,
	value,
	choices,
	handleFilterChange,
}) {
	let id = `id_${name}`
	return (
		<div className={"filters__field-row"}>
			<div className="filters__field-label">
				<label htmlFor={id}>{label}</label>
			</div>
			<select
				id={id}
				name={name}
				value={value}
				onChange={handleFilterChange}
			>
				<option value="">------</option>
				{choices.map(([value, choice]) => (
					<option
						key={value}
						value={value}
					>
						{choice}
					</option>
				))}
			</select>
		</div>
			)
}

function DatalistFilter({
	name,
	label,
	value,
	choices,
	handleFilterChange,
}) {
	let id = `id_${name}`
	let choicesId = `${name}_choices`

	return (
		<div className={"filters__field-row"}>
			<div className="filters__field-label">
				<label htmlFor={id}>{label}</label>
			</div>
			<input
				value={value}
				type="text"
				name={name}
				className="text-field--single"
				autoComplete="off"
				onChange={handleFilterChange}
				id={id}
				list={choicesId}
			/>

			<datalist
				id={choicesId}
			>
				{choices.map((choice, index) => (
					<option key={index} value={choice}></option>
				))}
			</datalist>
		</div>
	)
}

function RadioFilter({
	name,
	label,
	value,
	options,
	handleFilterChange,
}) {
	let id = `id_${name}`

	return (
		<div className={"filters__field-row"}>
			<div className="filters__field-label">
				{label}
			</div>

			<ul id={id}>
				{options.map( (option, index) => {
					let optionId = `id_${name}_${index}`
					return (
						<li key={option.value}>
							<label htmlFor={optionId}>
								<input
									type="radio"
									name={name}
									value={option.value}
									checked={value === option.value}
									id={optionId}
									onChange={handleFilterChange}
								/>
								{option.label}
							</label>
						</li>
					)
				})}
			</ul>
		</div>
	)
}

RadioFilter.defaultProps = {
	options: [
		{ label: 'Unknown', value: 'NOTHING' },
		{ label: 'Yes', value: 'JUST_TRUE' },
		{ label: 'No', value: 'JUST_FALSE' },
	],
}


export function BoolFilter(props) {
	return (
		<RadioFilter
			options={[
				{ label: 'Yes', value: '1' },
				{ label: 'No', value: '0' },
			]}
			{...props}
		/>
	)
}

export default function FilterSet({ filters, handleFilterChange, filterParameters, setFilterParameters }) {
	const components = filters.map((filter, index) => {
		if (filter.name === 'search') {
			return
		}
		if (filter.type === 'text') {
			return (
				<TextFilter
					key={index}
					name={filter.name}
					label={filter.title}
					value={filterParameters[filter.name].parameters || ""}
					handleFilterChange={handleFilterChange}
				/>
			)
		} else if (filter.type === 'date') {
			return (
				<DateFilter
					key={index}
					name={filter.name}
					label={filter.title}
					value={filterParameters[filter.name].parameters || {}}
					setFilterParameters={setFilterParameters}
				/>
			)
		} else if (filter.type === 'radio') {
			return (
				<RadioFilter
					key={index}
					name={filter.name}
					label={filter.title}
					value={filterParameters[filter.name].parameters || ""}
					handleFilterChange={handleFilterChange}
				/>
			)
		} else if (filter.type === 'bool') {
			return (
				<BoolFilter
					key={index}
					name={filter.name}
					label={filter.title}
					value={filterParameters[filter.name].parameters || ""}
					handleFilterChange={handleFilterChange}
				/>
			)
		} else if (filter.type === 'choice') {
			return (
				<SelectFilter
					key={index}
					name={filter.name}
					label={filter.title}
					choices={filter.choices}
					value={filterParameters[filter.name].parameters || ""}
					handleFilterChange={handleFilterChange}
				/>
			)
		} else if (filter.type == 'autocomplete') {
			return (
				<DatalistFilter
					key={index}
					name={filter.name}
					label={filter.title}
					choices={filter.choices}
					value={filterParameters[filter.name].parameters || ""}
					handleFilterChange={handleFilterChange}
				/>
			)
		} else {
			console.warn(`no filter defined for type "${filter.type}"`)
		}
	})
	return components
}



FilterSet.propTypes = {
	filters: PropTypes.array.isRequired,
	handleFilterChange: PropTypes.func.isRequired,
	filterParameters: PropTypes.object.isRequired,
}
