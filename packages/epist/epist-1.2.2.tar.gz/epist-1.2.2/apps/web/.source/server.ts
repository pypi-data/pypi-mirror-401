// @ts-nocheck
import * as __fd_glob_4 from "../content/docs/quickstart.md?collection=docs"
import * as __fd_glob_3 from "../content/docs/observability.md?collection=docs"
import * as __fd_glob_2 from "../content/docs/mcp_architecture.md?collection=docs"
import * as __fd_glob_1 from "../content/docs/integrations.md?collection=docs"
import * as __fd_glob_0 from "../content/docs/api_reference.md?collection=docs"
import { server } from 'fumadocs-mdx/runtime/server';
import type * as Config from '../source.config';

const create = server<typeof Config, import("fumadocs-mdx/runtime/types").InternalTypeConfig & {
  DocData: {
  }
}>({"doc":{"passthroughs":["extractedReferences"]}});

export const docs = await create.doc("docs", "content/docs", {"api_reference.md": __fd_glob_0, "integrations.md": __fd_glob_1, "mcp_architecture.md": __fd_glob_2, "observability.md": __fd_glob_3, "quickstart.md": __fd_glob_4, });

export const meta = await create.meta("meta", "content/docs", {});