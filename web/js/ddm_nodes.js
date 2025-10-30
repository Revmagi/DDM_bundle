// DDM Bundle - Set/Get Variable Nodes
// Modern ComfyUI-compatible implementation
// Handles frontend validation and type detection

import { app } from "../../../scripts/app.js";

function detectType(value) {
	if (value === null || value === undefined) return "*";
	if (typeof value === "number") return "FLOAT";
	if (typeof value === "string") return "STRING";
	if (typeof value === "boolean") return "BOOLEAN";
	if (value?.batch_index !== undefined) return "IMAGE";
	if (value?.samples !== undefined) return "LATENT";
	if (value?.cond !== undefined) return "CONDITIONING";
	if (value?.model !== undefined) return "MODEL";
	if (Array.isArray(value)) return "LIST";
	return "*";
}

// Register extension hooks
app.registerExtension({
	name: "DDM.Bundle.SetGetNodes",

	async setup() {
		// Initialize global variable storage
		if (!app.graph.DDM_globalVars) {
			app.graph.DDM_globalVars = {};
		}
	},

	async beforeRegisterNodeDef(nodeType, nodeData, app) {
		// Hook into DDM Set Node
		if (nodeData.name === "DDM_SetNode") {
			const onExecuted = nodeType.prototype.onExecuted;
			nodeType.prototype.onExecuted = function (message) {
				if (onExecuted) {
					onExecuted.apply(this, arguments);
				}

				// Store variable in graph scope
				const id = this.widgets?.find((w) => w.name === "id")?.value;
				if (id && message) {
					app.graph.DDM_globalVars = app.graph.DDM_globalVars || {};
					app.graph.DDM_globalVars[id] = message;

					// Update output type dynamically
					if (this.outputs && this.outputs[0] && message[0]) {
						const detectedType = detectType(message[0]);
						this.outputs[0].type = detectedType;
					}

					// Update node title
					this.title = `DDM Set (${id})`;
				}
			};

			// Add widget change handler
			const onNodeCreated = nodeType.prototype.onNodeCreated;
			nodeType.prototype.onNodeCreated = function () {
				if (onNodeCreated) {
					onNodeCreated.apply(this, arguments);
				}

				const idWidget = this.widgets?.find((w) => w.name === "id");
				if (idWidget) {
					const originalCallback = idWidget.callback;
					idWidget.callback = function (value) {
						if (originalCallback) {
							originalCallback.apply(this, arguments);
						}
						this.title = `DDM Set (${value})`;
					}.bind(this);
				}
			};
		}

		// Hook into DDM Get Node
		if (nodeData.name === "DDM_GetNode") {
			const onExecuted = nodeType.prototype.onExecuted;
			nodeType.prototype.onExecuted = function (message) {
				if (onExecuted) {
					onExecuted.apply(this, arguments);
				}

				// Retrieve variable from graph scope
				const id = this.widgets?.find((w) => w.name === "id")?.value;
				if (id) {
					app.graph.DDM_globalVars = app.graph.DDM_globalVars || {};
					const storedValue = app.graph.DDM_globalVars[id];

					// Update output type dynamically
					if (
						this.outputs &&
						this.outputs[0] &&
						storedValue &&
						storedValue[0]
					) {
						const detectedType = detectType(storedValue[0]);
						this.outputs[0].type = detectedType;
					}

					// Update node title
					this.title = `DDM Get (${id})`;
				}
			};

			// Add widget change handler
			const onNodeCreated = nodeType.prototype.onNodeCreated;
			nodeType.prototype.onNodeCreated = function () {
				if (onNodeCreated) {
					onNodeCreated.apply(this, arguments);
				}

				const idWidget = this.widgets?.find((w) => w.name === "id");
				if (idWidget) {
					const originalCallback = idWidget.callback;
					idWidget.callback = function (value) {
						if (originalCallback) {
							originalCallback.apply(this, arguments);
						}
						this.title = `DDM Get (${value})`;
					}.bind(this);
				}
			};
		}
	},

	async loadedGraphNode(node) {
		// Ensure titles are updated when loading saved workflows
		if (node.type === "DDM_SetNode" || node.type === "DDM_GetNode") {
			const id = node.widgets?.find((w) => w.name === "id")?.value;
			if (id) {
				const prefix = node.type === "DDM_SetNode" ? "DDM Set" : "DDM Get";
				node.title = `${prefix} (${id})`;
			}
		}
	},
});

console.log(
	"%c[DDM Bundle]%c Set/Get Variable nodes registered (Frontend)",
	"color: #42b983; font-weight: bold;",
	"color: inherit;"
);
