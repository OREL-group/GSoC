// Next.js API route support: https://nextjs.org/docs/api-routes/introduction
import { gql } from "@apollo/client";
import client from "../../lib/apollo-client";


export default function handler(req, res) {
  if (req.method === 'GET') {
    const { username } = req.query
    client.query({
      query: gql`
            query {
              user(login: "${username}") {
                name
              }

              viewer {
                repositories(first: 100, orderBy: { field: UPDATED_AT, direction: ASC }) {
                  nodes {
                    name
                    issues(states: OPEN) {
                      totalCount
                    }
                    url
                    isPrivate
                    owner {
                      login
                    }
                    defaultBranchRef {
                      name
                    }
                  }
                }
              }
            }
          `,
    })
      .then((response) => {
        // console.log(response)
        return res.json({ success: true, ...response.data });
      }).catch((err) => {
        // console.log(err)
        return res.json({ success: false, error: err });
      })
  }
}
