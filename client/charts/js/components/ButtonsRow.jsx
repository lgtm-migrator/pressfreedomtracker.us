import React from 'react'
import Button from './Button'

const labelStyle = {
	fontFamily: 'var(--font-base)',
	fontSize: '18px',
}

export default function ButtonsRow({
	label,
	buttonLabels,
	defaultSelection = null,
	updateSelection,
	isButtonSelectable,
	tooltipIfUnselectable = null,
}) {
	const [selectedButton, setSelectedButton] = React.useState(null)

	function changeSelectedButton(buttonLabel) {
		updateSelection(selectedButton === buttonLabel ? defaultSelection : buttonLabel)
		selectedButton === buttonLabel
			? setSelectedButton(defaultSelection)
			: setSelectedButton(buttonLabel)
	}

	return (
		<div style={{ display: 'flex', alignItems: 'center', margin: 12 }}>
			<div
				style={{
					...labelStyle,
				}}
			>
				{label}
			</div>
			<div style={{ marginLeft: 10 }}>
				{buttonLabels.map((buttonLabel) => (
					<Button
						label={buttonLabel}
						selected={
							(defaultSelection === buttonLabel && selectedButton === null) ||
							selectedButton === buttonLabel
						}
						onClick={() => {
							changeSelectedButton(buttonLabel)
						}}
						selectable={isButtonSelectable(buttonLabel)}
						tooltipIfUnselectable={tooltipIfUnselectable}
						key={buttonLabel}
					/>
				))}
			</div>
		</div>
	)
}
