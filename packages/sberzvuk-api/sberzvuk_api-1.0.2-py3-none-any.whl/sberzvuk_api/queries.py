GET_FULL_TRACK = """
query GetFullTrack(
    $ids: [ID!]!
    $withReleases: Boolean = false
    $withArtists: Boolean = false
) {
    getTracks(ids: $ids) {
        id
        title
        searchTitle
        position
        duration
        availability
        artistTemplate
        condition
        explicit
        lyrics
        zchan
        genres {
            id
            name
            shortName
        }
        collectionItemData {
            itemStatus
        }
        artists @include(if: $withArtists) {
            id
            title
            searchTitle
            description
            hasPage
            image {
                src
                palette
                paletteBottom
            }
            secondImage {
                src
                palette
                paletteBottom
            }
            animation {
                artistId
                effect
                image
                background {
                    type
                    image
                    color
                    gradient
                }
            }
        }
        release @include(if: $withReleases) {
            id
            title
            searchTitle
            type
            date
            image {
                src
                palette
                paletteBottom
            }
            genres {
                id
                name
                shortName
            }
            label {
                id
                title
            }
            availability
            artistTemplate
        }
        hasFlac
    }
}
"""

GET_PLAYLISTS = """
query GetPlaylists($ids: [ID!]!) {
	playlists(ids: $ids) {
		id
		title
		searchTitle
		updated
		description
		branded
		coverV1 {
			src
		}
		childParam
		image {
			src
			palette
			paletteBottom
		}
		isPublic
		duration
		isDeleted
		userId
		shared
		chart {
			trackId
			positionChange
		}
		collectionLastModified
		tracks {
			id
			credits
			title
			searchTitle
			position
			duration
			availability
			artistTemplate
			condition
			explicit
			lyrics
			hasFlac
			zchan
			artists {
				id
				title
			}
			release {
				id
				title
				image {
					src
					palette
					paletteBottom
				}
			}
		}
	}
}
"""

GET_RELEASES = """
query GetReleases(
    $ids: [ID!]!
	$withTracks: Boolean = false
	$withArtists: Boolean = false
) {
    getReleases(ids: $ids) {
        id
        title
        searchTitle
        type
        date
        image {
            src
            palette
            paletteBottom
        }
        genres {
            id
            name
            shortName
        }
        label {
            id
            title
        }
        availability
        artistTemplate
		artists @include(if: $withArtists) {
			id
			title
			searchTitle
			description
			hasPage
			image {
				src
				palette
				paletteBottom
			}
			secondImage {
				src
				palette
				paletteBottom
			}
			animation {
				artistId
				effect
				image
				background {
					type
					image
					color
					gradient
				}
			}
		}
        tracks @include(if: $withTracks) {
            id
            title
            searchTitle
            duration
            position
            availability
            artistTemplate
            condition
            explicit
            lyrics
            hasFlac
            zchan

            stream {
                expire
                expireDelta
                flac
                flacdrm
                high
                mid
            }

            artists {
                id
                title
            }

            release {
                id
                title
                image {
                    palette
                    paletteBottom
                    src
                }
            }
        }
    }
}
"""

GET_SEARCH_ALL = """
query GetSearchAll(
    $query: String
    $limit: Int = 2
    $trackCursor: Cursor = null
    $artistsCursor: Cursor = null
    $releasesCursor: Cursor = null
    $profilesCursor: Cursor = null
    $playlistsCursor: Cursor = null
    $episodesCursor: Cursor = null
    $booksCursor: Cursor = null
    $bookAuthorsCursor: Cursor = null
    $podcastsCursor: Cursor = null
    $tracks: Boolean = true
    $artists: Boolean = true
    $releases: Boolean = true
    $playlists: Boolean = true
    $profiles: Boolean = true
    $books: Boolean = true
    $bookAuthors: Boolean = true
    $episodes: Boolean = true
    $podcasts: Boolean = true
    $categories: Boolean = true
) {
    search(query: $query) {
        searchId
        tracks(limit: $limit, cursor: $trackCursor) @include(if: $tracks) {
            page {
                total
                prev
                next
                cursor
            }
            score
            items {
                id
                title
                availability
                explicit
                artistTemplate
                artists {
                    id
                    title
                }
                zchan
                availability
                condition
                duration
                release {
                    id
                    title
                    image {
                        src
                        palette
                        paletteBottom
                    }
                }
            }
        }
        artists(limit: $limit, cursor: $artistsCursor) @include(if: $artists) {
            page {
                total
                prev
                next
                cursor
            }
            score
            items {
                id
                title
                searchTitle
                description
                image {
                    src
                    palette
                    paletteBottom
                }
                profile {
                    id
                }
            }
        }
        releases(limit: $limit, cursor: $releasesCursor) @include(if: $releases) {
            page {
                total
                prev
                next
                cursor
            }
            score
            items {
                id
                title
                searchTitle
                explicit
                availability
                date
                artists {
                    id
                    title
                }
                image {
                    src
                    palette
                    paletteBottom
                }
            }
        }
        playlists(limit: $limit, cursor: $playlistsCursor) @include(if: $playlists) {
            page {
                total
                prev
                next
                cursor
            }
            score
            items {
                id
                title
                isPublic
                description
                duration
                tracks {
                    id
                    credits
                    title
                    searchTitle
                    position
                    duration
                    availability
                    artistTemplate
                    condition
                    explicit
                    lyrics
                    hasFlac
                    zchan
                    artists {
                        id
                        title
                    }
                    release {
                        id
                        title
                        image {
                            src
                            palette
                            paletteBottom
                        }
                    }
                }
                image {
                    src
                    palette
                    paletteBottom
                }
            }
        }
        profiles(limit: $limit, cursor: $profilesCursor) @include(if: $profiles) {
            page {
                total
                prev
                next
                cursor
            }
            score
            items {
                id
                name
                description
                image {
                    src
                }
            }
        }
        books(limit: $limit, cursor: $booksCursor) @include(if: $books) {
            page {
                total
                prev
                next
                cursor
            }
            score
            items {
                id
                title
                bookAuthors {
                    id
                    rname
                }
                image {
                    src
                }
            }
        }
        bookAuthors(limit: $limit, cursor: $bookAuthorsCursor) @include(if: $bookAuthors) {
            page {
                total
                prev
                next
                cursor
            }
            score
            items {
                id
                rname
                image {
                    src
                }
            }
        }
        episodes(limit: $limit, cursor: $episodesCursor) @include(if: $episodes) {
            page {
                total
                prev
                next
                cursor
            }
            score
            items {
                id
                title
                availability
                explicit
                duration
                publicationDate
                image {
                    src
                    palette
                    paletteBottom
                }
                podcast {
                    id
                    authors {
                        id
                        name
                    }
                    image {
                        src
                        palette
                        paletteBottom
                    }
                }
            }
        }
        podcasts(limit: $limit, cursor: $podcastsCursor) @include(if: $podcasts) {
            page {
                total
                prev
                next
                cursor
            }
            score
            items {
                id
                title
                explicit
                availability
                authors {
                    name
                }
                image {
                    src
                    palette
                    paletteBottom
                }
            }
        }
        categories(limit: 1) @include(if: $categories) {
            score
            items {
                id
                title
                description
                image {
                    src
                }
                webAction {
                    name
                    data {
                        url
                    }
                }
            }
        }
    }
}
"""


GET_SEARCH = """
query GetSearch($query: String, $limit: Int) {
  quickSearch(query: $query, limit: $limit) {
		content {
			__typename

			... on Track {
				id
				availability
				title
                artistTemplate
				artistNames
				release {
					image {
						src
                        palette
                        paletteBottom
                    }
				}
			}

			... on Artist {
				id
				title
				image {
					src
                    palette
                    paletteBottom
                }
				profile {
					id
				}
			}

			... on Release {
				id
				availability
				title
                artistTemplate
				artistNames
				date
				image {
					src
                    palette
                    paletteBottom
				}
			}

			... on Playlist {
				id
				isPublic
				title
				image {
					src
                    palette
                    paletteBottom
				}
				description
			}
		}
	}
}"""

GET_STREAM = """
query GetStream($ids: [ID!]!) {
	mediaContents(ids: $ids) {
        __typename
        
		... on Track {
			stream {
				expire
				expireDelta
				flacdrm
				high
				mid
			}
		}

		... on Episode {
			stream {
				expire
				expireDelta
				high
				mid
			}
		}

		... on Chapter {
			stream {
				expire
				expireDelta
				high
				mid
			}
		}
	}
}
"""

GET_TRACKS = """
query GetTracks($ids: [ID!]!) {
	getTracks(ids: $ids) {
		id
		title
		searchTitle
		position
		duration
		availability
		artistTemplate
		condition
		explicit
		lyrics
		zchan
		hasFlac
		artists {
			id
			title
			image {
				src
				palette
				paletteBottom
			}
		}
		release {
			id
			title
			image {
				src
				palette
				paletteBottom
			}
		}
	}
}
"""

ALL_QUERIES = {
    "GetFullTrack": GET_FULL_TRACK,
    "GetPlaylists": GET_PLAYLISTS,
    "GetReleases": GET_RELEASES,
    "GetSearch": GET_SEARCH,
    "GetSearchAll": GET_SEARCH_ALL,
    "GetStream": GET_STREAM,
    "GetTracks": GET_TRACKS,
}