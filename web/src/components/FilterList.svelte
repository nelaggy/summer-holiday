<script lang="ts">
	let {
		filterList,
		removedFilterList,
		suggestedFilterList,
		onUpdateFilters
	}: {
		filterList: string[];
		removedFilterList: string[];
		suggestedFilterList: string[];
		onUpdateFilters: (filters: string[], removedFilters: string[]) => void;
	} = $props();

    let filters = $state(filterList.map((f) => ({text: f, suggested: false})));
    let removedFilters = $state(removedFilterList.map((f) => ({text: f, suggested: false})));
    let suggestedFilters = $state(suggestedFilterList.map((f) => ({text: f, suggested: true})));
	let isCollapsed = $state(true);
	const toggleCollapse = () => {
		isCollapsed = !isCollapsed;
	};

	const addFilter = (filter: {text: string, suggested: boolean}) => {
		if (!filters.includes(filter)) {
			filters.push(filter);
			removedFilters = removedFilters.filter((f) => f !== filter);
		}
	};
    const addSuggestedFilter = (filter: {text: string, suggested: boolean}) => {
        if (!filters.includes(filter)) {
            filters.push(filter);
            suggestedFilters = suggestedFilters.filter((f) => f !== filter);
        }
    };
    const removeSuggestedFilter = (filter: {text: string, suggested: boolean}) => {
        if (!removedFilters.includes(filter)) {
            removedFilters.push(filter);
            suggestedFilters = suggestedFilters.filter((f) => f !== filter);
        }
    };
	const removeFilter = (filter: {text: string, suggested: boolean}) => {
		if (filters.includes(filter)) {
			filters = filters.filter((f) => f !== filter);
			removedFilters.push(filter);
		}
	};
	const updateFilters = () => {
		removedFilters.push(...suggestedFilters.filter((f) => !filters.includes(f)));
        filters = filters.map(f => ({text: f.text, suggested: false}));
        removedFilters = removedFilters.map(f => ({text: f.text, suggested: false}));
        suggestedFilters = []
		onUpdateFilters(filters.map(f => f.text), removedFilters.map(f => f.text));
	};
</script>

<div class='min-h-20'>
    <p>Filters</p>
{#each filters as filter}
	<div class="inline-flex items-center px-3 py-1 m-2 {filter.suggested ? 'border border-blue-500 text-blue-500' : 'bg-gray-200'} rounded-full">
		{filter.text}
		<button class="ml-3 {filter.suggested ? 'text-blue-500' :'text-gray-600'} hover:cursor-pointer" onclick={() => removeFilter(filter)}
			>x</button
		>
	</div>
{/each}
</div>
<div class='min-h-20'>
<p>Suggested Filters</p>
{#each suggestedFilters as filter}
    <div class="inline-flex items-center px-3 py-1 m-2 border border-blue-500 rounded-full">
        <span class="text-blue-500">{filter.text}</span>
        <button class="ml-3 text-blue-500 hover:cursor-pointer hover:text-blue-700" onclick={() => addSuggestedFilter(filter)}>
            +
        </button>
        <button class="ml-3 text-blue-500 hover:cursor-pointer hover:text-blue-700" onclick={() => removeSuggestedFilter(filter)}>
            x
        </button>
    </div>
{/each}
</div>
<div class="w-full min-h-20">
	<button class="w-full hover:cursor-pointer text-left" onclick={toggleCollapse}>
		{isCollapsed ? '+ Other Filters' : '- Hide Filters'}
	</button>
		<div class="w-full {isCollapsed ? 'invisible' : 'visible'}">
			{#each removedFilters as filter}
				<div class="inline-flex items-center px-3 py-1 m-2 {filter.suggested ? 'border border-blue-500 text-blue-500' : 'bg-gray-200'} rounded-full">
					{filter.text}
					<button class="ml-2 {filter.suggested ? 'text-blue-500' :'text-gray-600'} hover:cursor-pointer" onclick={() => addFilter(filter)}
					>
                        +
                    </button>
				</div>
			{/each}
		</div>
</div>
<div class='w-full flex flex-row justify-end'>
    <button class="bg-cyan-500 text-white p-2 rounded-2xl mt-4 hover:cursor-pointer hover:bg-cyan-700" onclick={updateFilters}>
        Update Filters
    </button>
</div>