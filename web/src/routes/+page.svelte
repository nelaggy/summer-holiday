<script lang="ts">
	import StartForm from '../components/StartForm.svelte';

    let ai_flag = $state(false);
	const onNewTrip = (params: {
		destination: string;
		startDate: string;
		endDate: string;
		numAdults: number;
		numChildren: number;
		budget: number;
		notes: string;
	}) => {
        ai_flag = true;
		// call api
	};
</script>

<div class="flex items-center justify-center h-screen bg-gray-100">
	<div class="flex flex-col items-center bg-white p-8 rounded-lg shadow-lg w-4xl">
		<h1 class="text-4xl mb-4">Plan your next adventure</h1>
		<StartForm newTrip={onNewTrip} />
	</div>
</div>
