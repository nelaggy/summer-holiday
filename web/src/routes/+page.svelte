<script lang="ts">
	import FilterList from '../components/FilterList.svelte';
	import StartForm from '../components/StartForm.svelte';

	let ai_flag = $state(false);
	let loading = $state(false);
	let params = $state({
		destination: '',
		startDate: '',
		endDate: '',
		numAdults: 0,
		numChildren: 0,
		budget: 0,
		notes: ''
	});
	let filters: string[] = $state([]);
	let removedFilters: string[] = $state([]);
	let suggestedFilters: string[] = $state([]);
	let num_results = $state(0);
    let results: any[] = $state([]);

	const callApi = async () => {
		loading = true;
		const response = await fetch('http://localhost:8000/search', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
					location: params.destination,
					checkin_date: params.startDate,
					checkout_date: params.endDate,
					adults_number: params.numAdults,
					children_number: params.numChildren,
					budget: params.budget,
					dynamic_filters: [params.notes, ...filters],
				full_results: false
			})
		});
		// await new Promise((resolve) => setTimeout(resolve, 1000));

		// const data = {
		// 	num_results: 100,
		// 	suggestedFilters: ['a', 'b', 'c', 'd', 'e', 'f']
		// };
		const data = await response.json();
		num_results = data.num_results;
		suggestedFilters = data.suggested_filters;
		loading = false;
	};

    const getResults = async () => {
        loading = true;
        const response = await fetch('http://localhost:8000/search?full_results=1', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
					location: params.destination,
					checkin_date: params.startDate,
					checkout_date: params.endDate,
					adults_number: params.numAdults,
					children_number: params.numChildren,
					budget: params.budget,
					dynamic_filters: [params.notes, ...filters]
			})
		});
		// await new Promise((resolve) => setTimeout(resolve, 1000));

		// const data = {
		// 	results: [
        //         {
        //             id: 1,
        //             hotel_name: 'Hotel A',
        //             gross_amount: 100,
        //             url: 'https://booking.com',
        //             address: 'Location A'
        //         },
        //         {
        //             id: 2,
        //             hotel_name: 'Hotel B',
        //             gross_amount: 150,
        //             url: 'https://google.com',
        //             location: 'Location B'
        //         }
        //     ]
		// };
		const data = await response.json();
        console.log(data)
		results = data.results;
		loading = false;
	};
        
	const onUpdateParams = (newParams: {
		destination: string;
		startDate: string;
		endDate: string;
		numAdults: number;
		numChildren: number;
		budget: number;
		notes: string;
	}) => {
		params = newParams;
		ai_flag = true;
        suggestedFilters = [];
        results = [];
		callApi();
	};

	const onUpdateFilters = (newFilters: string[], newRemovedFilters: string[]) => {
		filters = newFilters;
		removedFilters = newRemovedFilters;
		suggestedFilters = [];
        results = [];
		console.log(newFilters, newRemovedFilters);
		callApi();
	};
</script>

<div class="flex items-center justify-center h-screen bg-gray-100">
	<div class="flex flex-col items-center bg-white p-8 rounded-lg shadow-lg w-4xl">
		<h1 class="text-4xl mb-4">Plan your next adventure</h1>
		<StartForm updateParams={onUpdateParams} />
		{#if ai_flag}
			{#if loading}
				<div class="flex items-center">
					<svg class="animate-grow h-5 w-5 mr-3 text-blue-500" viewBox="0 0 24 24">
						<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"
						></circle>
						<circle class="opacity-75" cx="12" cy="12" r="5" fill="currentColor">
							<animate attributeName="r" values="5;10;5" dur="1s" repeatCount="indefinite" />
						</circle>
					</svg>
					<span class="text-gray-700">Loading...</span>
				</div>
			{:else}
				<div class="mt-4 w-full">
					<p>We've found over <b>{num_results}</b> options.</p>
					<FilterList
						filterList={filters}
						removedFilterList={removedFilters}
						suggestedFilterList={suggestedFilters}
						{onUpdateFilters}
					/>
				</div>
                {#if results.length > 0}
                <div class="mt-4 w-full h-60 overflow-y-scroll">
                    <h2 class="text-2xl mb-4">Options</h2>
                    <ul>
                        {#each results as result}
                        <a href={result.url} target="_blank" class="block">
                            <li class="border-b border-gray-300 py-2">
                                <h3 class="text-xl">{result.hotel_name}</h3>
                                <p>Price: {result.gross_amount.amount_rounded}</p>
                                <p>Location: {result.address}</p>
                            </li>
                        </a>
                        {/each}
                    </ul>
                </div>
            {:else}
                <button class="bg-blue-500 text-white p-2 rounded-lg mt-4" onclick={getResults}>
                    Show me my options
                </button>
            {/if}
			{/if}
            
		{/if}
	</div>
</div>
