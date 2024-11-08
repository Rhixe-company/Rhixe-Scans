import htmx from 'htmx.org';
import Sortable from 'sortablejs';

window.htmx = htmx;

htmx.config.defaultSwapStyle = 'outerHTML';
htmx.config.historyEnabled = true;
htmx.config.historyCacheSize = 0;
htmx.config.refreshOnHistoryMiss = true;
htmx.config.useTemplateFragments = true;
htmx.config.globalViewTransitions = true;
htmx.config.selfRequestsOnly = true;
htmx.config.allowScriptTags = true;
htmx.config.ignoreTitle = true;
htmx.onLoad((content: { querySelectorAll: (arg0: string) => NodeListOf<Element> }) => {
	const sortables = content.querySelectorAll('.sortable');

	for (let i = 0; i < sortables.length; i++) {
		const sortable = sortables[i];

		new Sortable(sortable as HTMLElement, {
			animation: 150,
			ghostClass: 'blue-background-class',
		});
	}
});
