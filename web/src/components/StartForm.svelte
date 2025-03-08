<script lang="ts">
	const {
		newTrip
	}: {
		newTrip: (params: {
			destination: string;
			startDate: string;
			endDate: string;
			numAdults: number;
			numChildren: number;
			budget: number;
			notes: string;
		}) => void;
	} = $props();
	let minDate = new Date().toISOString().split('T')[0];
	let stage: number = $state(0);
	let destination: string = $state('');
	let startDate: string = $state('');
	let endDate: string = $state('');
	let numAdults: number = $state(0);
	let numChildren: number = $state(0);
	let budget: number = $state(0);
	let notes: string = $state('');

	const nextStage = () => {
		if (stage <= 4) {
			stage++;
		}
	};

	const prevStage = () => {
		if (stage > 0) {
			stage--;
		}
	};
</script>

<div class="grid grid-cols-6 gap-4 mt-2 w-full items-start">
	{#if stage == 0}
		<form
			class="grid col-span-6 grid-cols-subgrid"
			onsubmit={(e) => {
				e.preventDefault();
				nextStage();
			}}
		>
			<label for="destination" class="col-span-1 my-auto text-xl align-middle pr-2">Where?</label>
			<div class="col-span-5 flex grow">
				<input
					bind:value={destination}
					id="destination"
					type="text"
					placeholder="Destination"
					autocomplete="off"
					required
					class="border border-stone-500 p-2 rounded-l-2xl focus:outline-none focus:ring-2 focus:ring-blue-500 w-full"
					disabled={stage != 0}
				/>
				<button
					class="bg-cyan-600 text-white p-2 rounded-r-2xl focus:outline-none focus:ring-2 focus:ring-blue-500 hover:cursor-pointer disabled:cursor-default disabled:bg-cyan-100"
					type="submit"
					disabled={!destination}
				>
					Go
				</button>
			</div>
		</form>
	{:else}
		<p class="my-auto text-xl align-middle pr-2 col-span-1">My trip to</p>
		<p class="text-xl text-stone-500 col-span-5">{destination}</p>
	{/if}
	{#if stage == 1}
		<form
			class="grid col-span-6 grid-cols-subgrid gap-4"
			onsubmit={(e) => {
				e.preventDefault();
				nextStage();
			}}
		>
			<label for="date" class="my-auto text-xl align-middle pr-2 col-span-1">When?</label>
			<div class="col-span-5 flex">
				<input
					bind:value={startDate}
					placeholder="From"
					type="date"
					id="date"
					min={minDate}
					max={endDate}
					required
					onfocus={({ currentTarget }) => {
						currentTarget!.showPicker();
					}}
					class="border-l border-t border-b border-stone-500 p-2 rounded-l-2xl focus:outline-none focus:ring-2 focus:ring-blue-500 grow"
				/>
				<label
					for="end-date"
					class="my-auto text-xl align-middle text-center p-2 border-t border-b border-stone-500"
					>to</label
				>
				<input
					bind:value={endDate}
					id="end-date"
					placeholder="To"
					type="date"
					min={startDate || minDate}
					required
					onfocus={({ currentTarget }) => {
						currentTarget!.showPicker();
					}}
					class="border-r border-b border-t border-stone-500 p-2 rounded-r-2xl focus:outline-none focus:ring-2 focus:ring-blue-500 grow"
				/>
			</div>
			<div class="col-span-6 grid grid-cols-subgrid">
				<button
					class="bg-white col-span-1 text-black p-2 rounded-2xl focus:outline-none focus:ring-2 focus:ring-blue-500 hover:cursor-pointer col-start-5"
					type="reset"
					onclick={prevStage}
				>
					Back
				</button>
				<button
					class="bg-cyan-600 col-span-1 text-white p-2 rounded-2xl focus:outline-none focus:ring-2 focus:ring-blue-500 hover:cursor-pointer disabled:cursor-default disabled:bg-cyan-100 col-start-6"
					type="submit"
					disabled={!startDate || !endDate}
				>
					Next
				</button>
			</div>
		</form>
	{:else if stage > 1}
		<p class="my-auto text-xl align-middle pr-2 col-span-1">from</p>
		<p class="text-xl text-stone-500 col-span-5">{startDate} to {endDate}</p>
	{/if}
	{#if stage == 2}
		<form
			class="grid col-span-6 grid-cols-subgrid gap-4"
			onsubmit={(e) => {
				e.preventDefault();
				nextStage();
			}}
		>
			<p class="my-auto text-xl align-middle pr-2 col-span-1">Who?</p>
			<input
				bind:value={numAdults}
				id="adults"
				type="number"
				min={0}
				defaultValue={0}
				autocomplete="off"
				required
				class="border border-stone-500 p-2 rounded-2xl focus:outline-none focus:ring-2 focus:ring-blue-500 w-full col-span-1 text-center"
			/>
			<label for="adults" class="my-auto text-lg pr-2 col-span-1">adults</label>
			<p class="my-auto text-lg text-center pr-2 col-span-1">&</p>
			<input
				bind:value={numChildren}
				id="children"
				type="number"
				min={0}
				autocomplete="off"
				required
				defaultValue={0}
				class="border border-stone-500 p-2 rounded-2xl focus:outline-none focus:ring-2 focus:ring-blue-500 w-full col-span-1 text-center"
			/>
			<label for="children" class="my-auto text-lg align-middle pr-2 col-span-1">children</label>
			<div class="col-span-6 grid grid-cols-subgrid">
				<button
					class="bg-white col-span-1 text-black p-2 rounded-2xl focus:outline-none focus:ring-2 focus:ring-blue-500 hover:cursor-pointer col-start-5"
					type="reset"
					onclick={prevStage}
				>
					Back
				</button>
				<button
					class="bg-cyan-600 col-span-1 text-white p-2 rounded-2xl focus:outline-none focus:ring-2 focus:ring-blue-500 hover:cursor-pointer disabled:cursor-default disabled:bg-cyan-100 col-start-6"
					type="submit"
					disabled={numAdults == 0 && numChildren == 0}
				>
					Next
				</button>
			</div>
		</form>
	{:else if stage > 2}
		<p class="my-auto text-xl align-middle pr-2 col-span-1">for</p>
		<p class="text-xl text-stone-500 col-span-5">
			{numAdults} adults and {numChildren} children
		</p>
	{/if}
	{#if stage == 3}
		<form
			class="grid col-span-6 grid-cols-subgrid gap-4"
			onsubmit={(e) => {
				e.preventDefault();
				nextStage();
			}}
		>
			<p class="my-auto text-xl align-middle pr-2 col-span-1">Budget?</p>
			<input
				bind:value={budget}
				id="budget"
				type="number"
				min={0}
				autocomplete="off"
				placeholder="Budget"
				required
				class="border border-stone-500 p-2 rounded-2xl focus:outline-none focus:ring-2 focus:ring-blue-500 col-span-3 text-center"
			/>
			<label for="budget" class="my-auto text-lg align-middle pr-2 col-span-2 text-right"
				>GBP per person</label
			>
			<div class="col-span-6 grid grid-cols-subgrid">
				<button
					class="bg-white col-span-1 text-black p-2 rounded-2xl focus:outline-none focus:ring-2 focus:ring-blue-500 hover:cursor-pointer col-start-5"
					type="reset"
					onclick={prevStage}
				>
					Back
				</button>
				<button
					class="bg-cyan-600 col-span-1 text-white p-2 rounded-2xl focus:outline-none focus:ring-2 focus:ring-blue-500 hover:cursor-pointer disabled:cursor-default disabled:bg-cyan-100 col-start-6"
					type="submit"
					disabled={!budget}
				>
					Next
				</button>
			</div>
		</form>
	{:else if stage > 3}
		<p class="my-auto text-xl align-middle pr-2 col-span-1">with</p>
		<p class="text-xl text-stone-500 col-span-5">a budget of {budget} GBP per person</p>
	{/if}
	{#if stage == 4}
		<form
			class="grid col-span-6 grid-cols-subgrid gap-4"
			onsubmit={(e) => {
				e.preventDefault();
				nextStage();
				newTrip({ destination, startDate, endDate, numAdults, numChildren, budget, notes });
			}}
		>
			<p class="my-auto text-xl align-middle pr-2 col-span-1">Notes?</p>
			<input
				bind:value={notes}
				id="notes"
				type="text"
				placeholder="Anything else?"
				autocomplete="off"
				class="border border-stone-500 p-2 rounded-2xl focus:outline-none focus:ring-2 focus:ring-blue-500 col-span-5"
			/>
			<button
				class="mt-8 bg-cyan-600 col-span-2 text-white p-2 rounded-2xl focus:outline-none focus:ring-2 focus:ring-blue-500 hover:cursor-pointer col-start-3"
				type="submit"
			>
				Plan my trip!
			</button>
		</form>
	{:else if stage > 4}
		{#if notes}
			<p class="my-auto text-xl align-middle pr-2 col-span-1">and</p>
			<p class="text-xl text-stone-500 col-span-5">{notes}</p>
		{/if}
	{/if}
</div>
